create table Discount_Codes(
 code_id INT NOT NULL  AUTO_INCREMENT,
   code VARCHAR(30) NOT NULL,
   expire_date DATE,
   discount Float,
   fetcheduser_id INT,
   brand_id INT NOT NULL,
   PRIMARY KEY (code_id) 
);
