from flask import Flask, request, jsonify
import os
from model_service import service_get_train_test_labels_count, service_get_testset_infos, service_get_testset_instance_info, service_get_correct_count_of_labelset
from label_mapping_service import get_label_mapping_val


app = Flask(__name__, static_url_path='/static')

#--------- view dispatching --------

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/statistic')
def statistic():
    return app.send_static_file('statistic.html')

@app.route('/test_cases')
def test_cases():
    return app.send_static_file('test_case.html')
    

# -------- API --------

@app.route('/api/testset/instances', methods=['GET'])
def get_testset_instances():
    instance_list = list()
    testset_instance_infos, testset_predicts = service_get_testset_infos()
    
    for instance_id in testset_predicts.keys():
        detail = dict()
        info = testset_instance_infos[instance_id]
        detail['id'] = instance_id
        detail['class1'] = info[0]
        detail['class2'] = info[1]
        detail['class3'] = info[2]
        detail['class4'] = info[3]
        detail['content'] = info[4]
        pred_info = testset_predicts[instance_id]
        detail['true_agency'] = get_label_mapping_val(pred_info[0])
        detail['pred_agency'] = get_label_mapping_val(pred_info[1])
        instance_list.append(detail)

    response = dict({'data' : instance_list})
    return jsonify(response)



@app.route('/api/testset/instance', methods=['GET'])
def get_analysis_data():
    selected_instance_id = int(request.args.get('instance_id'))
    info, pred_info = service_get_testset_instance_info(selected_instance_id)

    detail = dict()
    detail['class1'] = info[0]
    detail['class2'] = info[1]
    detail['class3'] = info[2]
    detail['class4'] = info[3]
    detail['content'] = info[4]
    detail['agency'] = info[5]
    detail['true_label'] = pred_info[0]
    detail['pred_label'] = pred_info[1]

    return jsonify(detail)



@app.route('/api/statistic/train_test', methods=['GET'])
def get_train_test_set_statistic():
    sta_labels, sta_train_label_count, sta_test_label_count = service_get_train_test_labels_count()
    
    sta_accuracy = list()
    for index in range(len(sta_labels)):
        label = sta_labels[index]
        sta_label_correct_count = service_get_correct_count_of_labelset(label)
        accuracy = sta_label_correct_count / sta_test_label_count[index]
        sta_accuracy.append(accuracy)

    sta_agencies = list()
    for label in sta_labels:
        agency = get_label_mapping_val(label)
        if agency.endswith('公司'):
            agency = agency[: 3] + 'com.'
        sta_agencies.append(agency)

    response = dict()
    response['agencies'] = sta_agencies
    response['trainset_count'] = sta_train_label_count
    response['testset_count'] = sta_test_label_count
    response['accuracy'] = sta_accuracy

    return jsonify(response)




if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=8080)
