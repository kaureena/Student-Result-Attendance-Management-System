-- Dimension: assessment component
CREATE TABLE IF NOT EXISTS dim_assessment_component (
  component_key SERIAL PRIMARY KEY,
  component_name TEXT UNIQUE NOT NULL
);
