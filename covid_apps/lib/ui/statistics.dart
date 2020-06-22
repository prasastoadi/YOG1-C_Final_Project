import 'package:bangkit_covid_detection/api/case_detail.dart';
import 'package:bangkit_covid_detection/api/http_service.dart';
import 'package:flutter/material.dart';

class StatisticsPage extends StatelessWidget {
  final HttpService httpService = HttpService();

  String formatDetail(String s) {
    String res = '';
    int c = 0;
    for (int i = s.length - 1; i >= 0; i--) {
      c++;
      res = s[i] + res;
      if (c % 3 == 0) res = ',' + res;
    }
    return res;
  }

  Widget banner(String title, String jumlah, Color color) {
    return Container(
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.all(Radius.circular(30)),
      ),
      padding: EdgeInsets.all(20),
      child: Column(
        children: [
          Text(title,
              style: TextStyle(
                color: Colors.white,
                fontSize: 18,
              )),
          SizedBox(height: 30),
          Text(jumlah,
              style: TextStyle(
                color: Colors.white,
                fontSize: 18,
              )),
        ],
      ),
    );
  }

  List<Widget> caseWidget(CaseDetail detail) {
    return [
      Expanded(
        flex: 1,
        child: banner(
          'Confirmed',
          (detail.confirmed < 0)
              ? '???'
              : formatDetail(detail.confirmed.toString()),
          Colors.orange,
        ),
      ),
      SizedBox(width: 10),
      Expanded(
        flex: 1,
        child: banner(
          'Recovered',
          (detail.recover < 0)
              ? '???'
              : formatDetail(detail.recover.toString()),
          Colors.green,
        ),
      ),
      SizedBox(width: 10),
      Expanded(
        flex: 1,
        child: banner(
          'Death',
          (detail.death < 0) ? '???' : formatDetail(detail.death.toString()),
          Colors.red,
        ),
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 40),
      decoration: BoxDecoration(
        color: Colors.blue.shade800,
        borderRadius: BorderRadius.vertical(bottom: Radius.circular(30)),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Statistics',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.all(Radius.circular(20)),
                ),
                padding: EdgeInsets.all(10),
                child: Text('Indonesia',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 18,
                    )),
              ),
            ],
          ),
          SizedBox(height: 20),
          FutureBuilder(
            future: httpService.getPosts(),
            builder: (BuildContext context, AsyncSnapshot<CaseDetail> snap) {
              if (snap.hasData) {
                CaseDetail detail = snap.data;
                return Row(
                  children: caseWidget(detail),
                );
              } else {
                CaseDetail detail =
                    CaseDetail(confirmed: -1, death: -1, recover: -1);
                return Row(
                  children: caseWidget(detail),
                );
              }
            },
          ),
        ],
      ),
    );
  }
}
