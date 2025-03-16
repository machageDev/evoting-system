import 'package:flutter/material.dart';

class Dashboard extends StatelessWidget {
  const Dashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("E-Voting Dashboard"),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              // Navigate to settings
            },
          ),
          IconButton(
            icon: const Icon(Icons.exit_to_app),
            onPressed: () {
              // Handle logout
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Welcome message or dashboard overview
            const Text(
              "Welcome to the E-Voting Dashboard",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),

            // Stats Overview (e.g., Elections, Voters, Votes)
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _dashboardCard("Elections", "3 Active", Icons.event),
                _dashboardCard("Voters", "500", Icons.group),
                _dashboardCard("Votes Cast", "300", Icons.check_circle),
              ],
            ),

            const SizedBox(height: 20),

            // Quick Actions Section
            const Text(
              "Quick Actions",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _actionButton("Create Election", Icons.add),
                _actionButton("Add Candidate", Icons.person_add),
                _actionButton("Register Voter", Icons.person_outline),
              ],
            ),

            const SizedBox(height: 20),

            // Recent Activity Section
            const Text(
              "Recent Activity",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            _recentActivity("Election '2025' created", "March 15, 2025"),
            _recentActivity("Candidate 'John Doe' added", "March 14, 2025"),
            _recentActivity("Voter 'Jane Doe' registered", "March 13, 2025"),
          ],
        ),
      ),
    );
  }

  // Dashboard Card for Stats Overview
  Widget _dashboardCard(String title, String value, IconData icon) {
    return Card(
      color: Colors.blue.shade100,
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 40, color: Colors.blue),
            const SizedBox(height: 10),
            Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 5),
            Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  // Quick Action Button
  Widget _actionButton(String title, IconData icon) {
    return ElevatedButton.icon(
      onPressed: () {
        // Navigate to corresponding page
      },
      icon: Icon(icon),
      label: Text(title),
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        textStyle: const TextStyle(fontSize: 16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }

  // Recent Activity Item
  Widget _recentActivity(String description, String date) {
    return ListTile(
      leading: const Icon(Icons.notifications),
      title: Text(description),
      subtitle: Text(date),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      onTap: () {
        // Navigate to the detailed activity page
      },
    );
  }
}
