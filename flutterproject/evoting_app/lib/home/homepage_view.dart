import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('eVoting - Home'),
        automaticallyImplyLeading: false, // Removes back button
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              Navigator.pushReplacementNamed(context, '/login');
            },
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            const Text(
              'Election Results',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            _buildResultsSection(),

            const Divider(height: 30),

            const Text(
              'Available Elections',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            _buildElectionsList(context),
          ],
        ),
      ),
    );
  }

  Widget _buildResultsSection() {
    // Replace with your real election results fetching logic
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: const [
        ListTile(
          title: Text('Presidential Election'),
          subtitle: Text('Winner: Candidate A'),
        ),
        ListTile(
          title: Text('Senate Election'),
          subtitle: Text('Winner: Candidate B'),
        ),
      ],
    );
  }

  Widget _buildElectionsList(BuildContext context) {
    // Replace with your real elections list fetching logic
    return Column(
      children: [
        Card(
          elevation: 4,
          child: ListTile(
            title: const Text('Presidential Election'),
            subtitle: const Text('Status: Open'),
            trailing: ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/vote');
              },
              child: const Text('Vote'),
            ),
          ),
        ),
        Card(
          elevation: 4,
          child: ListTile(
            title: const Text('Senate Election'),
            subtitle: const Text('Status: Closed'),
            trailing: ElevatedButton(
              onPressed: null, // Voting closed
              child: const Text('Closed'),
            ),
          ),
        ),
      ],
    );
  }
}
