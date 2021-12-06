from strongbox.database.settings import ACCOUNT_TABLE, VAULT_TABLE


def create_tables(db):
    cursor = db.cursor()
    # Create account table:
    cursor.execute(
        f"""CREATE TABLE {ACCOUNT_TABLE}(
  name VARCHAR(25),
  username SMALLINT UNSIGNED,
  mail VARCHAR(30),
  password VARCHAR(100),
  vault_id SMALLINT UNSIGNED,
  account_id SMALLINT UNSIGNED,
  PRIMARY KEY (name, username, mail)
)"""
    )
    # Create vault table:
    cursor.execute(
        f"""CREATE TABLE {VAULT_TABLE}(
hashed_password VARCHAR(64),
id SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY (id, hashed_password)
)"""
    )
    db.commit()
