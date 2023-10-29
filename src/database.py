import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# to run local
# SQLALCHEMY_DATABASE_URL = ('postgresql://vetclinic_user:aGliabvr0EnH2f8H2aQ8pFqxmbjmEwbm@dpg-ckuml53amefc73b38u2g-a'
#                            '.frankfurt-postgres.render.com/vetclinic_db')
# to run on render.com
SQLALCHEMY_DATABASE_URL = ('postgresql://vetclinic_user:aGliabvr0EnH2f8H2aQ8pFqxmbjmEwbm@dpg-ckuml53amefc73b38u2g-a'
                           '/vetclinic_db')


dogs_data = {
    'name': ['Bob', 'Marli', 'Snoopy', 'Rex', 'Pongo', 'Tillman', 'Uga'],
    'pk': list(range(7)),
    'kind': ['terrier', 'bulldog', 'dalmatian', 'dalmatian', 'dalmatian', 'bulldog', 'bulldog']
}


timestamps_data = {
    'id': [0, 1],
    'timestamp': [12, 10]
}

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# populate database with existing data
for data_name, data in zip(
        ['dogs', 'timestamps'],
        [dogs_data, timestamps_data]
):
    df = pd.DataFrame.from_dict(data)
    df.to_sql(data_name, engine, index=False, if_exists='replace')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
