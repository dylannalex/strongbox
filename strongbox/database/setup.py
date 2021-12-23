from mysql.connector.connection_cext import CMySQLConnection
from strongbox.database.settings import ACCOUNT_TABLE, VAULT_TABLE


def create_tables(db: CMySQLConnection) -> None:
    cursor = db.cursor()
    # Create account table:
    cursor.execute(
        f"""CREATE TABLE {ACCOUNT_TABLE}(
  name VARCHAR(25),
  username VARCHAR(30),
  mail VARCHAR(50),
  password VARCHAR(600),
  vault_id SMALLINT UNSIGNED,
  account_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (account_id)
);"""
    )
    # Create vault table:
    cursor.execute(
        f"""CREATE TABLE {VAULT_TABLE}(
hashed_password VARCHAR(64) UNIQUE,
salt VARCHAR(16),
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)
);"""
    )
    db.commit()
