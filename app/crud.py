from sqlalchemy.orm import Session
import models, schemas


def create_dog(db: Session, dog: schemas.Dog):
    db_dog = models.Dog(**dog.model_dump())
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog


def get_dog(db: Session, dog_pk: int):
    return db.query(models.Dog).filter(models.Dog.pk == dog_pk).first()


def get_dogs(db: Session, kind: str = None):
    if kind:
        return db.query(models.Dog).filter(models.Dog.kind == kind).all()
    else:
        return db.query(models.Dog).all()


def update_dog(db: Session, dog: schemas.Dog):
    db_dog = db.query(models.Dog).filter(models.Dog.pk == dog.pk).first()
    db_dog.name = dog.name
    db_dog.kind = dog.kind
    db_dog.pk = dog.pk
    db.commit()
    db.refresh(db_dog)
    return db_dog


def create_timestamp(db: Session, timestamp: schemas.Timestamp):
    db_timestamp = models.Timestamp(**timestamp.model_dump())
    db.add(db_timestamp)
    db.commit()
    db.refresh(db_timestamp)
    return db_timestamp


def get_timestamp(db: Session, timestamp_id: int):
    return db.query(models.Timestamp).filter(models.Timestamp.id == timestamp_id).first()
