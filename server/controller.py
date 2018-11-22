from flask import Flask, request, jsonify
import os
from model_service import service_get_testset_labels_count, service_get_testset_infos, service_get_testset_instance_info

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return app.send_static_file('index.html')
    

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
        detail['true_label'] = pred_info[0]
        detail['pred_label'] = pred_info[1]
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






if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=8080)
