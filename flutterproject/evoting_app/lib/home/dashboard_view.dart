import 'package:evoting_app/manage/manage_candidate_view.dart';
import 'package:evoting_app/manage/manageelection_view.dart';
import 'package:evoting_app/home/voterdashboard_view.dart';
import 'package:flutter/material.dart';

class DashboardView extends StatefulWidget {
  const DashboardView({super.key});

  @override
  _DashboardViewState createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  int _selectedIndex = 0;

  static const List<Widget> _widgetOptions = <Widget>[
    VoterDashboardView(),
    ManageElectionsView(),
    ManageCandidatesView(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _onSettingsSelected() {
    // Navigate to the settings page
    Navigator.pushNamed(context, '/settings');
  }

  void _onProfileSelected() {
    // Navigate to the profile page
    Navigator.pushNamed(context, '/profile');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard | E-Voting'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: _onSettingsSelected,
          ),
          IconButton(
            icon: const Icon(Icons.account_circle),
            onPressed: _onProfileSelected,
            
          ),
        ],
      ),
      body: _widgetOptions.elementAt(_selectedIndex),
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
        onTap: _onItemTapped,
      ),
    );
  }
}
