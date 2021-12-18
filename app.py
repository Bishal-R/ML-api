import numpy as np
from flask import Flask, request, jsonify, render_template,send_file
import pickle
import pandas as pd
import json
from io import BytesIO
import csv
import io
from process import estimate
import warnings
warnings.filterwarnings('ignore')
warnings.warn('DelftStack')
warnings.warn('Do not show this message')
app = Flask(__name__)
# this will clena the url data and return as clean DataFrame
def col_reset(df):
    column_name=df.iloc[0]
    col_lis=[]
    for i in column_name:
        col_lis.append(i)
    drop_df=df.drop(index=df.index[0], axis=0,inplace=True)
    my_df=df.set_axis(col_lis, axis=1)
    final_df=my_df.reset_index(drop=True)
    return final_df
@app.route("/training",methods=['POST'])
def training():
    csv_file=request.files['file']
    target_col=request.form['target_col']
    label_col=request.form.getlist('predict_val')
    stream = io.TextIOWrapper(csv_file.stream._file, "UTF8", newline=None)
    data=[]
    csv_input = csv.reader(stream)
    for row in csv_input:
        data.append(row)
    dfdf=pd.DataFrame(data=data)
    df_reset=col_reset(dfdf)
    dict_df=df_reset.to_dict()
    for col in df_reset:
        if col.lower()=="id":
            df_reset.drop(columns=col,inplace=True)
        else:
            df_reset=df_reset
    return_model,best_mdl_dict,all_mdl_dict=estimate(df_reset,target_col)
    model_data=pickle.dumps(return_model)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    return send_file(BytesIO(model_data),attachment_filename='model',as_attachment=True)

@app.route('/testing',methods=['POST'])
def testing():
        upload_model=request.files['upload_model']
        # label_col=request.form['input_val']
        # inputs=[i for i in label_col.split(',')]
        my_mdl=pickle.load(upload_model)
        # predict_val=my_mdl.predict([[label_col]])
        return jsonify({"testing":"ok"})

if __name__ == "__main__":
    app.run(debug=True)