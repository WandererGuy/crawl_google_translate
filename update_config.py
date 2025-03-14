import yaml

def read_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_yaml_config(config, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(config, file, sort_keys=False)

if __name__ == "__main__":
    # Step 1: Read
    config_data = read_yaml_config("config.yaml")
    print("Original config:", config_data)

    # Step 2: Update
    config_data["previous_output_dir_num"] = str(int(config_data["current_output_dir_num"]))
    config_data["current_output_dir_num"] = str(int(config_data["current_output_dir_num"]) + 1)

    # Step 3: Write
    write_yaml_config(config_data, "config.yaml")

    print("Updated config:", read_yaml_config("config.yaml"))
