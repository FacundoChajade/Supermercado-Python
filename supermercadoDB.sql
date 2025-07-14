DROP DATABASE IF EXISTS supermercado;
CREATE DATABASE supermercado;
USE supermercado;

CREATE TABLE producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    cantidad INT(4) NOT NULL,
    precio DECIMAL(5,2) NOT NULL
);

CREATE TABLE pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni_cliente INT NOT NULL,
    precio_final DECIMAL(7,2)
);

CREATE TABLE producto_de_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    pedido_id INT,
    cantidad_pedida INT(4),
    cantidad_recibida INT(4),
    FOREIGN KEY (producto_id) REFERENCES producto(id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id)
);

INSERT INTO producto (nombre, cantidad, precio) VALUES
('Fideos', 20, 1.50),
('Arroz', 30, 2.00),
('Agua', 30, 1.00),
('Whisky', 30, 25.00),
('Aceite', 20, 5.00),
('Don Satur', 15, 1.25),
('Prime XS', 10, 2.50),
('Opera', 30, 1.75);

DELIMITER //
CREATE TRIGGER restar_productos
BEFORE INSERT ON producto_de_pedido
FOR EACH ROW
BEGIN
  DECLARE cantidad_actual INT;
  SELECT cantidad INTO cantidad_actual FROM producto WHERE id = NEW.producto_id;

  IF cantidad_actual < NEW.cantidad_pedida THEN
    SET NEW.cantidad_recibida = cantidad_actual;
    UPDATE producto SET cantidad = 0 WHERE id = NEW.producto_id;
  
  ELSE
    SET NEW.cantidad_recibida = NEW.cantidad_pedida;
    UPDATE producto SET cantidad = cantidad - NEW.cantidad_pedida WHERE id = NEW.producto_id;
    
  END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE calcular_precio_total(IN pedidoId INT)
BEGIN
	DECLARE total DECIMAL(10,2);

    SELECT SUM(pdp.cantidad_recibida * p.precio) INTO total FROM producto_de_pedido pdp JOIN producto p ON pdp.producto_id = p.id WHERE pdp.pedido_id = pedidoId;

    UPDATE pedido SET precio_final = total WHERE id = pedidoId;
END;
//
DELIMITER ;