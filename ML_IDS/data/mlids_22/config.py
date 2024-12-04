
Strategy = {
    'type_1': {
        'throttle_intervals': [5, 10, 15, 20],
        'max_dl': ['10 Mbps', '5 Mbps', '3 Mbps', '1 Mbps'],
        'max_ul': ['10 Mbps', '5 Mbps', '3 Mbps', '1 Mbps'],
        'qos': [20, 30, 40, 50],
        'pdu_session_deletion_limit': 25 
    },

    'type_2': {
        'throttle_intervals': [30, 70, 100, 130],
        'max_dl': ['5 Mbps', '3 Mbps', '1 Mbps', '500 Kbps'],
        'max_ul': ['5 Mbps', '3 Mbps', '1 Mbps', '500 Kbps'],
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

## Return the strategy based on tye
def get_enforcment_strategy(type='type_1'):
    return Strategy.get(type)


