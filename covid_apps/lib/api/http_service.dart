import 'dart:convert';

import 'package:bangkit_covid_detection/api/case_detail.dart';
import 'package:http/http.dart';

class HttpService {
  final String mainURL = 'https://indonesia-covid-19-api.now.sh/api';

  Future<CaseDetail> getPosts() async {
    Response res = await get(mainURL);

    if (res.statusCode == 200) {
      dynamic body = jsonDecode(res.body);
      CaseDetail posts = CaseDetail.fromJSON(body);
      return posts;
    } else {
      throw "Can't get data.";
    }
  }
}
