CREATE TABLE file_info (
  file_id INT PRIMARY KEY AUTO_INCREMENT,
  file_name VARCHAR(255) NOT NULL,
  file_size INT NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  creation_time DATETIME NOT NULL,
  modification_time DATETIME NOT NULL,
  access_time DATETIME NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  owner VARCHAR(50) NOT NULL,
  permissions VARCHAR(20) NOT NULL,
  file_tags VARCHAR(255),
  external_link VARCHAR(255),
  notes TEXT
);