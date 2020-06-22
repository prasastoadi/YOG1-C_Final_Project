import 'dart:io';

import 'package:dotted_border/dotted_border.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:tflite/tflite.dart';

class DiagnosePage extends StatefulWidget {
  @override
  _DiagnosePageState createState() => _DiagnosePageState();
}

class _DiagnosePageState extends State<DiagnosePage> {
  File imageURI;
  String result = '';
  String path;
  double dimension = 300;

  Future pickImage() async {
    var image = await ImagePicker().getImage(source: ImageSource.gallery);
    if (image == null) return;
    path = image.path;
    imageURI = File(path);
    print(path);
    classifyImage();
  }

  Future classifyImage() async {
    await Tflite.loadModel(
        model: 'assets/tflite/model.tflite',
        labels: 'assets/tflite/labels.txt');
    var output = await Tflite.runModelOnImage(path: path);
    setState(() {
      result = getLabel(output[0]);
      // result = output[0].toString();
    });
  }

  String getLabel(var map) {
    String res = map['label'];
    return res.split(' ')[1];
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 30),
      padding: EdgeInsets.symmetric(horizontal: 30, vertical: 20),
      decoration: BoxDecoration(
        color: Colors.blue,
        borderRadius: BorderRadius.all(Radius.circular(30)),
      ),
      child: Column(
        children: [
          Container(
            alignment: Alignment.centerLeft,
            child: Text('Are you feeling bad?',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                )),
          ),
          SizedBox(height: 10),
          Text(
            'Check your lung rontgen result here. It can predict about infected covid',
            style: TextStyle(
              color: Colors.black,
              fontSize: 16,
            ),
          ),
          SizedBox(height: 30),
          Center(
            child: DottedBorder(
              borderType: BorderType.RRect,
              radius: Radius.circular(12),
              padding: EdgeInsets.all(10),
              child: GestureDetector(
                onTap: () => pickImage(),
                child: ClipRRect(
                  borderRadius: BorderRadius.all(Radius.circular(12)),
                  child: (imageURI == null)
                      ? Container(
                          color: Colors.blue,
                          width: dimension,
                          height: dimension,
                          alignment: Alignment.center,
                          child: Text('Select image'),
                        )
                      : Image.file(
                          imageURI,
                          width: dimension,
                          height: dimension,
                          fit: BoxFit.cover,
                        ),
                ),
              ),
            ),
          ),
          (result.isEmpty)
              ? Container()
              : Container(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      SizedBox(height: 20),
                      Text(
                        result,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: (result == 'Positive')
                              ? Colors.red
                              : Colors.green,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 10),
                    ],
                  ),
                ),
        ],
      ),
    );
  }
}
