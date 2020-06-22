// <a href='https://www.freepik.com/free-photos-vectors/medical'>Medical vector created by freepik - www.freepik.com</a>
// <a href='https://www.freepik.com/free-photos-vectors/hand'>Hand vector created by freepik - www.freepik.com</a>
// <a href='https://www.freepik.com/free-photos-vectors/people'>People vector created by freepik - www.freepik.com</a>

import 'package:flutter/material.dart';

class PreventionPage extends StatelessWidget {
  Widget pict(String file, String desc) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(20)),
          child: Image.asset(
            file,
            width: 140,
            height: 140,
          ),
        ),
        SizedBox(height: 10),
        Text(
          desc,
          textAlign: TextAlign.center,
          style: TextStyle(
            color: Colors.black,
            fontSize: 16,
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 30),
      color: Colors.white,
      child: Column(
        children: [
          Container(
            alignment: Alignment.centerLeft,
            child: Text(
              'Prevention',
              style: TextStyle(
                color: Colors.black,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              pict('assets/images/distancing.jpg', 'Keep social\ndistancing'),
              pict('assets/images/mask.jpg', 'Always wear\na mask'),
              pict('assets/images/wash.jpg', 'Wash the hands\noften'),
            ],
          ),
        ],
      ),
    );
  }
}
