import logging
import os

from fastapi import FastAPI, Request, Depends, Form, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from . import models, crud, github, schemas, kanboard
from .database import engine, SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add session middleware for flash messages
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24).hex())

templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request, 
    tag: str | None = None, 
    sort_by: str = 'stargazers_count', 
    sort_order: str = 'desc', 
    db: Session = Depends(get_db)
):
    repos = crud.get_all_repos(db, tag=tag, sort_by=sort_by, sort_order=sort_order)

    # Get flash message from session for full page loads
    flash_message = request.session.pop('flash', None)

    template_vars = {
        "request": request,
        "repos": repos,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "selected_tag": tag,
        "flash_message": flash_message
    }

    if "HX-Request" in request.headers:
        # For HTMX requests, return only the table partial.
        return templates.TemplateResponse("_repo_table.html", template_vars)

    # For initial page loads, return the full page
    all_tags = crud.get_all_tags(db)
    template_vars["all_tags"] = all_tags
    return templates.TemplateResponse("index.html", template_vars)

@app.post("/sync", response_class=RedirectResponse)
async def sync_stars(request: Request, db: Session = Depends(get_db)):
    logging.info("Starting star sync process...")
    try:
        starred_repos_data = github.get_starred_repos()
        logging.info(f"Fetched {len(starred_repos_data)} repos from GitHub.")
        repos_to_create = [schemas.RepositoryCreate(**repo) for repo in starred_repos_data]
        
        new_repo_count = crud.batch_create_repos(db, repos=repos_to_create)
        logging.info(f"Finished processing repos. {new_repo_count} new repos were added.")
        
        if new_repo_count > 0:
            request.session['flash'] = f"Sync complete! Added {new_repo_count} new repositories."
        else:
            request.session['flash'] = "No new starred repositories found, or all are already up to date."

    except Exception as e:
        logging.error(f"An error occurred during sync: {e}", exc_info=True)
        request.session['flash'] = f"An error occurred during sync: {e}"
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/repos/{repo_id}/tags", response_class=HTMLResponse)
async def update_tags(request: Request, repo_id: int, tags: str = Form(...), db: Session = Depends(get_db)):
    crud.update_repo_tags(db, repo_id=repo_id, tags=tags)
    repo = db.query(models.Repository).filter(models.Repository.id == repo_id).first()
    request.session['flash'] = f"Tags for {repo.full_name} updated successfully!"
    return templates.TemplateResponse("_repo_tags.html", {"request": request, "repo": repo})

@app.post("/repos/{repo_id}/create-ticket")
async def create_ticket_for_repo(
    request: Request,
    repo_id: int,
    db: Session = Depends(get_db)
):
    repo = crud.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    title = f"Review Starred Repo: {repo.full_name}"
    description = f"URL: {repo.url}\n\nDescription: {repo.description or 'N/A'}\n\nTags: {repo.tags or 'None'}"
    
    tags = [tag.strip() for tag in repo.tags.split(",")] if repo.tags else []

    try:
        task_id = kanboard.create_kanboard_task(title=title, description=description, tags=tags)
        request.session['flash'] = f"Successfully created Kanboard ticket #{task_id} for {repo.full_name}."
    except Exception as e:
        logging.error(f"Failed to create Kanboard ticket for repo {repo.id}: {e}")
        request.session['flash'] = f"Error: Could not create Kanboard ticket. {e}"

    # This endpoint is called via HTMX but we don't need to return any content,
    # just set the flash message, which will be displayed on the next page refresh/load.
    # A 204 No Content response is appropriate here.
    return Response(status_code=204)
