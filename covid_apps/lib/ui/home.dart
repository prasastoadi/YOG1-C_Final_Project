import 'package:bangkit_covid_detection/ui/diagnose.dart';
import 'package:bangkit_covid_detection/ui/prevention.dart';
import 'package:bangkit_covid_detection/ui/statistics.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.white,
        child: ListView(
          children: [
            StatisticsPage(),
            PreventionPage(),
            DiagnosePage(),
          ],
        ),
      ),
    );
  }
}
