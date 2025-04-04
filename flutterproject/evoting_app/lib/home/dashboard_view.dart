// ignore_for_file: non_constant_identifier_names

import 'package:evoting_app/manage/manage_candidate_view.dart';
import 'package:evoting_app/manage/manageelection_view.dart';
import 'package:evoting_app/home/voterdashboard_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';


class DashboardView extends StatefulWidget {
  const DashboardView({super.key});

  @override
  _DashboardViewState createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  int _selectedIndex = 0;

  static final List<Widget> _widgetOptions = <Widget>[
    VoterDashboardView(),
    ManageElectionsView(),
    ManageCandidatesView(),
  ];

  void _onSettingsSelected() {
    Navigator.pushNamed(context, '/settings');
  }

  void _onProfileSelected() {
    Navigator.pushNamed(context, '/profile');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard | E-Voting'),
        automaticallyImplyLeading: false, 
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: _onSettingsSelected,
          ),
           GestureDetector(
            onTap: _onProfileSelected,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: CircleAvatar(
                radius: 18,
                backgroundColor: Colors.transparent,
                child: SvgPicture.asset(
                  "assets/img/undraw_profile_2.svg",
                  width: 36,
                  height: 36,
                  placeholderBuilder: (context) => Icon(Icons.account_circle, size: 36),
                ),
              ),
            ),
          ),
        ],
      ),
      body: _widgetOptions[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: 'Voter Dashboard',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.how_to_vote),
            label: 'Manage Elections',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Manage Candidates',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.blue,
        onTap: (index) {
          // Prevent reloading when tapping the same tab
          if (_selectedIndex != index) {
            setState(() {
              _selectedIndex = index;
            });
          }
        },
      ),
    );
  }
}
