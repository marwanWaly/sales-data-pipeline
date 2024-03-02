CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` integer PRIMARY KEY ON CONFLICT IGNORE,
  `name` varchar(255),
  `username` varchar(255),
  `email` varchar(255),
  `lat` float,
  `lng` float,
  `temp` float,
  `feels_like` float,
  `temp_min` float,
  `temp_max` float,
  `pressure` float,
  `humidity` float,
  `sea_level` float,
  `grnd_level` float,
  `weather_condition` varchar(20),
  `created_at` timestamp default CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS `sales` (
  `order_id` integer,
  `customer_id` integer,
  `product_id` integer,
  `quantity` float,
  `price` float,
  `order_date` timestamp,
  `created_at` timestamp default CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  PRIMARY KEY (order_id, customer_id, product_id) ON CONFLICT IGNORE
);
