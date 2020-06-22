import 'package:bangkit_covid_detection/ui/splashscreen.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

const String appName = 'Covid Manager';

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: appName,
      home: SplashScreenPage(),
    );
  }
}
