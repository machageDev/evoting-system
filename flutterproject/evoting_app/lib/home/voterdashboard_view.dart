import 'package:flutter/material.dart';
import 'package:evoting_app/Api/api_service.dart';

class VoterDashboardView extends StatefulWidget {
  const VoterDashboardView({super.key});

  @override
  State<VoterDashboardView> createState() => _VoterDashboardViewState();
}

class _VoterDashboardViewState extends State<VoterDashboardView> {
  Map<String, dynamic>? voterInfo;
  List<dynamic> elections = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchVoterDashboard();
  }

Future<void> fetchVoterDashboard() async {
  try {
    final response = await ApiService.getVoterDashboard();

    if (response == null) {
      // Handle null response gracefully
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
      return;
    }

    if (mounted) {
      setState(() {
        voterInfo = response['voter'] ?? {};  // Ensure voterInfo is never null
        elections = response['elections'] ?? [];
        isLoading = false;
      });
    }
  } catch (error) {
    print("Error fetching voter dashboard: $error");
    if (mounted) {
      setState(() {
        isLoading = false;
      });
    }
  }
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Voter Dashboard")),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Voter Info
                  if (voterInfo != null)
                    Card(
                      elevation: 3,
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text("Name: ${voterInfo!['name']}",
                                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                            Text("Username: ${voterInfo!['username']}",
                                style: const TextStyle(fontSize: 16)),
                            Text("Age: ${voterInfo!['age']}",
                                style: const TextStyle(fontSize: 16)),
                          ],
                        ),
                      ),
                    ),

                  const SizedBox(height: 16),

                  // Voting Section
                  ElevatedButton.icon(
                    onPressed: () {
                      Navigator.pushNamed(context, '/vote');
                    },
                    icon: const Icon(Icons.how_to_vote),
                    label: const Text("Cast Your Vote"),
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                  ),

                  const SizedBox(height: 16),

                  // View Results Section
                  ElevatedButton.icon(
                    onPressed: () {
                      Navigator.pushNamed(context, '/results');
                    },
                    icon: const Icon(Icons.bar_chart),
                    label: const Text("View Results"),
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                  ),

                  const SizedBox(height: 24),

                  // Active Elections List
                  Text("Active Elections", style: Theme.of(context).textTheme.titleLarge),
                  const Divider(),
                  elections.isEmpty
                      ? const Center(child: Text("No active elections."))
                      : ListView.builder(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: elections.length,
                          itemBuilder: (context, index) {
                            final election = elections[index];
                            return Card(
                              child: ListTile(
                                title: Text(election['name']),
                                subtitle: Text("Date: ${election['election_date']}"),
                                trailing: election['status'] == 'active'
                                    ? ElevatedButton(
                                        onPressed: () {
                                          Navigator.pushNamed(context, '/vote', arguments: election['id']);
                                        },
                                        child: const Text("Vote"),
                                      )
                                    : const Text("Closed", style: TextStyle(color: Colors.grey)),
                              ),
                            );
                          },
                        ),
                ],
              ),
            ),
    );
  }
}
