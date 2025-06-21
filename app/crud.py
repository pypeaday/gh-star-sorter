from sqlalchemy.orm import Session
import logging

from . import models, schemas


def get_repo_by_repo_id(db: Session, repo_id: int):
    return db.query(models.Repository).filter(models.Repository.repo_id == repo_id).first()

def get_all_repos(db: Session, skip: int = 0, limit: int = 1000, tag: str | None = None, sort_by: str = 'stargazers_count', sort_order: str = 'desc'):
    query = db.query(models.Repository)
    if tag:
        query = query.filter(models.Repository.tags.like(f"%{tag}%"))

    sort_column = getattr(models.Repository, sort_by, models.Repository.stargazers_count)
    
    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
        
    return query.offset(skip).limit(limit).all()



def update_repo_tags(db: Session, repo_id: int, tags: str):
    db_repo = db.query(models.Repository).filter(models.Repository.id == repo_id).first()
    if db_repo:
        db_repo.tags = tags
        db.commit()
        db.refresh(db_repo)
    return db_repo

def batch_create_repos(db: Session, repos: list[schemas.RepositoryCreate]):
    logging.info("Starting batch create process...")
    existing_repo_ids = {repo[0] for repo in db.query(models.Repository.repo_id).all()}
    logging.info(f"Found {len(existing_repo_ids)} existing repos in the database.")

    new_repos = []
    for repo_data in repos:
        if repo_data.repo_id not in existing_repo_ids:
            new_repos.append(models.Repository(**repo_data.model_dump()))

    logging.info(f"Found {len(new_repos)} new repos to add.")

    if new_repos:
        logging.info("Committing new repos to the database...")
        db.bulk_save_objects(new_repos)
        db.commit()
        logging.info("Commit successful.")

    logging.info("Batch create process finished.")
    return len(new_repos)

def get_all_tags(db: Session):
    all_tags_list = db.query(models.Repository.tags).filter(models.Repository.tags.isnot(None)).all()
    tags = set()
    for row in all_tags_list:
        repo_tags = [t.strip() for t in row[0].split(',') if t.strip()]
        tags.update(repo_tags)
    return sorted(list(tags))
