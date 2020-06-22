import 'package:flutter/foundation.dart';

class CaseDetail {
  final int confirmed;
  final int recover;
  final int death;

  CaseDetail({
    @required this.confirmed,
    @required this.death,
    @required this.recover,
  });

  factory CaseDetail.fromJSON(Map<String, dynamic> json) {
    return CaseDetail(
      confirmed: json['jumlahKasus'],
      death: json['meninggal'],
      recover: json['sembuh'],
    );
  }
}
