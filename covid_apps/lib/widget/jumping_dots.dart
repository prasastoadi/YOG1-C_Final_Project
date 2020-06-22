import 'package:flutter/material.dart';
import 'package:flutter/animation.dart';

class _JumpingDot extends AnimatedWidget {
  final Color color;
  final double dotSize;
  _JumpingDot({Key key, Animation<double> animation, this.color, this.dotSize})
      : super(key: key, listenable: animation);

  Widget build(BuildContext context) {
    final Animation<double> animation = listenable;
    return Container(
      height: 15.0,
      child: Column(
        children: <Widget>[
          SizedBox(
            height: 8.0 - animation.value,
          ),
          Container(
            height: dotSize,
            width: dotSize,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
          ),
        ],
      ),
    );
  }
}

class JumpingDotsProgressIndicator extends StatefulWidget {
  final int numberOfDots;
  final double dotSize;
  final double dotSpacing;
  final Color color;
  final double completionDuration;
  final double beginTweenValue = 0.0;
  final double endTweenValue = 8.0;

  JumpingDotsProgressIndicator({
    this.numberOfDots = 3,
    this.dotSize = 10.0,
    this.color = Colors.white,
    this.dotSpacing = 0.0,
    this.completionDuration = 3.0,
  });

  _JumpingDotsProgressIndicatorState createState() =>
      _JumpingDotsProgressIndicatorState(
        numberOfDots: this.numberOfDots,
        dotSize: this.dotSize,
        color: this.color,
        dotSpacing: this.dotSpacing,
        completionDuration: this.completionDuration,
      );
}

class _JumpingDotsProgressIndicatorState
    extends State<JumpingDotsProgressIndicator> with TickerProviderStateMixin {
  int numberOfDots;
  int milliseconds;
  double completionDuration;
  double dotSize;
  double dotSpacing;
  Color color;
  List<AnimationController> controllers = new List<AnimationController>();
  List<Animation<double>> animations = new List<Animation<double>>();
  List<Widget> _widgets = new List<Widget>();

  _JumpingDotsProgressIndicatorState({
    this.numberOfDots,
    this.dotSize,
    this.color,
    this.dotSpacing,
    this.completionDuration,
  }) {
    milliseconds =
        (2000.0 * completionDuration) ~/ (numberOfDots.toDouble() + 3.0);
  }

  initState() {
    super.initState();
    // print("mulai");
    for (int i = 0; i < numberOfDots; i++) {
      _addAnimationControllers();
      _buildAnimations(i);
      _addListOfDots(i);
    }
    print(_widgets.length);
    controllers[0].forward();
  }

  void _addAnimationControllers() {
    controllers.add(AnimationController(
        duration: Duration(milliseconds: milliseconds), vsync: this));
  }

  void _addListOfDots(int index) {
    _widgets.add(Padding(
      padding: EdgeInsets.only(right: dotSpacing),
      child: _JumpingDot(
        animation: animations[index],
        dotSize: dotSize,
        color: color,
      ),
    ));
  }

  void _buildAnimations(int index) {
    animations.add(
        Tween(begin: widget.beginTweenValue, end: widget.endTweenValue)
            .animate(controllers[index])
              ..addStatusListener((AnimationStatus status) {
                if (status == AnimationStatus.completed)
                  controllers[index].reverse();
                if (index == numberOfDots - 1 &&
                    status == AnimationStatus.dismissed) {
                  controllers[0].forward();
                }
                if (animations[index].value > widget.endTweenValue / 2 &&
                    index < numberOfDots - 1) {
                  controllers[index + 1].forward();
                }
              }));
  }

  Widget build(BuildContext context) {
    return Row(mainAxisAlignment: MainAxisAlignment.center, children: _widgets);
  }

  dispose() {
    for (int i = 0; i < numberOfDots; i++) controllers[i].dispose();
    super.dispose();
  }
}
