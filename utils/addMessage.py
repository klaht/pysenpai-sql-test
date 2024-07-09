import yaml

def dump_data_to_yaml(object, file):
    for key, value in object.items():
        file.write(key + ":\n")
        sorted_msgs = dict(sorted(value.items()))
        for msg_key, msg in sorted_msgs.items():
            file.write("  " + msg_key + ": |-\n    ")
            file.write(msg.replace("\n", "\n    ") + "\n")



if __name__ == "__main__":
    msg_key = input("Insert message key to add: ")
    msg_fi = input("Insert message in FI: ")
    msg_en = input("Insert message in EN: ")
    msg_parent = input("Insert message parent (program by default): ")
    if msg_parent == "":
        msg_parent = "program"

    with open(f"../pysenpai-sql/pysenpai_sql/msg_data/en/messages.yml", 'r') as f:
        data = yaml.safe_load(f)
    
    data[msg_parent][msg_key] = msg_en
    if data:
        with open(f"../pysenpai-sql/pysenpai_sql/msg_data/en/messages.yml", 'w') as f:
            dump_data_to_yaml(data, f)

    with open(f"../pysenpai-sql/pysenpai_sql/msg_data/fi/messages.yml", 'r') as f:
        data = yaml.safe_load(f)
    
    data[msg_parent][msg_key] = msg_fi
    if data:
        with open(f"../pysenpai-sql/pysenpai_sql/msg_data/fi/messages.yml", 'w') as f:
            dump_data_to_yaml(data, f)
    