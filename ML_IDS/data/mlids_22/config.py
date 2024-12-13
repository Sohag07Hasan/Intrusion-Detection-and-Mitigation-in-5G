
Strategy = {
    'type_1': {
        'policy': 'attack_count',
        'throttle_intervals': [30, 60, 90, 120],
        'max_dl': ['60 Kbps', '40 Kbps', '20 Kbps', '0.00001 Kbps'],
        'max_ul': ['60 Kbps', '40 Kbps', '20 Kbps', '0.00001 Kbps'],
        'qos': [20, 30, 40, 50],
        'pdu_session_deletion_limit': 150 
    },

    'type_2': {
        'policy': 'attack_duration',
        'throttle_intervals': [30, 60, 90, 120],
        'max_dl': ['60 Kbps', '40 Kbps', '20 Kbps', '0.00001 Kbps'],
        'max_ul': ['60 Kbps', '40 Kbps', '20 Kbps', '0.00001 Kbps'],
        'qos': [20, 30, 40, 50],
        'pdu_session_deletion_limit': 150
    },

}

SavedFiles = {
    'cntx_mapping': './mapping_data.txt',
    'attack_records': './attack_records.csv',
    'dataset': './overlap_dataset_live.csv'
}


##IP address of UEs
MS_IP_POOL = ['10.60.0.0/24', '10.61.0.0/24', '10.62.0.0/24']

## Defining File Name
ATTACK_RECORD = './attack_records.csv'


## Return the strategy based on tye
def get_enforcment_strategy(type='type_1'):
    return Strategy.get(type)


