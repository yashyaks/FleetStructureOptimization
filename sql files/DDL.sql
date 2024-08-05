-- fleet_data.carbon_emissions definition

CREATE TABLE `carbon_emissions` (
  `year` int DEFAULT NULL,
  `carbon_emission` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- fleet_data.cost_profiles definition

CREATE TABLE `cost_profiles` (
  `end_of_year` int DEFAULT NULL,
  `resale_value_percent` int DEFAULT NULL,
  `insurance_cost_percent` bigint DEFAULT NULL,
  `maintenance_cost_percent` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- fleet_data.demand definition

CREATE TABLE `demand` (
  `year` int DEFAULT NULL,
  `size` varchar(2) DEFAULT NULL,
  `distance` varchar(2) DEFAULT NULL,
  `demand` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- fleet_data.fuels definition

CREATE TABLE `fuels` (
  `fuel` varchar(255) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `emissions_co2_per_unit_fuel` float DEFAULT NULL,
  `cost_per_unit_fuel` float DEFAULT NULL,
  `cost_uncertainty_percent` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- fleet_data.vehicles definition

CREATE TABLE `vehicles` (
  `id` text,
  `vehicle` text,
  `size` text,
  `year` bigint DEFAULT NULL,
  `cost` int DEFAULT NULL,
  `yearly_range` int DEFAULT NULL,
  `distance` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- fleet_data.vehicles_fuels definition

CREATE TABLE `vehicles_fuels` (
  `id` text,
  `fuel` text,
  `consumption_unitfuel_per_km` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;