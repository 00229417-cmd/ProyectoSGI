-- schema_users.sql
-- Tabla users (login separado)
-- Compatible MySQL / MariaDB
CREATE TABLE IF NOT EXISTS users (
  id_user INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(200),
  email VARCHAR(150),
  role VARCHAR(50) DEFAULT 'user',
  active TINYINT(1) DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

