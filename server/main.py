from flask import Flask
from flask_cors import CORS
from flask import request
from app import generate_html2o
from app import multifileCreator
from githubHandler import main
from app import makeChangesOnTheCode

app = Flask(__name__)

CORS(app=app)


@app.route('/makeApplication',methods=['POST'])
def initApplication():
    data = request.get_json()
    prompt = data['prompt']
    generate_html2o(prompt)
    global jsonData
    jsonData=  multifileCreator()
    if jsonData:
        if type(jsonData)=='str':
            return {'status':400,'msg': 'opps! something went wrong please try again later'}
        success= main()
        if success:
            return {'status':200,'msg':f'the code has been updated at {success}'}
        return {'status':400,'msg': 'opps! something went wrong please try again later'}

@app.route('/editProject',methods=['POST'])
def makeEdit():
    data = request.get_json()
    prompt = data['prompt']
    if jsonData:
        if makeChangesOnTheCode(jsonData,prompt):
            success = main()
            if success:
                return {'status':200,'msg':f'the code has been updated at {success}'}
        return {'status':400,'msg': 'opps! something went wrong please try again later'}
    return {
            'msg': 'you got to wrong page bud! please create the project first'
        }




app.run(debug=True,port=5000)