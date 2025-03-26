// ignore_for_file: library_private_types_in_public_api

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class DashboardView extends StatefulWidget {
  const DashboardView({super.key});

  @override
  _DashboardViewState createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  String username = '';
  List activeElections = [];
  List pendingElections = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchDashboardData();
  }

  Future<void> fetchDashboardData() async {
    final url = Uri.parse('http://192.168.0.54:8000/api/dashboard');

    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print("API Response: $data"); // Debugging step

        setState(() {
          username = data['user'] != null ? data['user']['username'] : "Guest";
          activeElections = data['active_elections'] ?? [];
          pendingElections = data['pending_elections'] ?? [];
          isLoading = false;
        });
      } else {
        print('Failed to load dashboard data: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching dashboard data: $e');
    }
  }

  void _onMenuSelected(String value) {
    switch (value) {
      case 'election_results':
        Navigator.pushNamed(context, '/manage_election');
        break;
      case 'voter_dashboard':
        Navigator.pushNamed(context, '/voterDashboard');
        break;
      case 'view_candidates':
        Navigator.pushNamed(context, '/manage_candidate');
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard | E-Voting'),
        actions: [
          PopupMenuButton<String>(
            onSelected: _onMenuSelected,
            itemBuilder: (context) => [
              PopupMenuItem(value: 'election_results', child: Text('Election Results')),
              PopupMenuItem(value: 'voter_dashboard', child: Text('Voter Dashboard')),
              PopupMenuItem(value: 'view_candidates', child: Text('View Candidates')),
            ],
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Text("Home", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  Icon(Icons.arrow_drop_down),
                ],
              ),
            ),
          )
        ],
      ),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Welcome, $username!',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  SizedBox(height: 10),
                  Text('Ready to participate in elections? See active and pending elections below.'),
                  SizedBox(height: 20),

                  // Active Elections
                  Text('🗳️ Active Elections',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  SizedBox(height: 10),
                  activeElections.isEmpty
                      ? Text('No active elections at the moment.')
                      : Column(
                          children: activeElections.map((election) {
                            return Card(
                              margin: EdgeInsets.only(bottom: 10),
                              child: Padding(
                                padding: EdgeInsets.all(12),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(election['title'],
                                        style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.bold)),
                                    SizedBox(height: 5),
                                    Text('Ends on: ${election['end_date']}'),
                                    SizedBox(height: 10),
                                    ElevatedButton(
                                      onPressed: () {
                                        print('Vote in Election ID: ${election['id']}');
                                      },
                                      child: Text('Vote Now'),
                                    )
                                  ],
                                ),
                              ),
                            );
                          }).toList(),
                        ),

                  SizedBox(height: 20),

                  // Pending Elections
                  Text('⏳ Pending Elections',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  SizedBox(height: 10),
                  pendingElections.isEmpty
                      ? Text('No pending elections at the moment.')
                      : Column(
                          children: pendingElections.map((election) {
                            return Card(
                              margin: EdgeInsets.only(bottom: 10),
                              child: Padding(
                                padding: EdgeInsets.all(12),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(election['title'],
                                        style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.bold)),
                                    SizedBox(height: 5),
                                    Text('Starts on: ${election['start_date']}'),
                                  ],
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                ],
              ),
            ),
    );
  }
}
