
Strategy = {
    'type_1': {
        'throttle_intervals': [60, 120, 180, 240, 300, 330, 360, 390, 420, 450],
        'max_dl': ['3 Mbps', '2 Mbps', '2.5 Mbps', '2 Mbps', '1.5 Mbps', '1 Mbps', '500 Kbps', '200 Kbps', '100 Kbps', '50 Kbps'],
        'max_ul': ['3 Mbps', '2 Mbps', '2.5 Mbps', '2 Mbps', '1.5 Mbps', '1 Mbps', '500 Kbps', '200 Kbps', '100 Kbps', '50 Kbps'],
        'qos': [20, 40, 60, 80, 100, 110, 120, 130, 140, 150],
        'pdu_session_deletion_limit': 500 
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


