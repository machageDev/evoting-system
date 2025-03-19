import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:fl_chart/fl_chart.dart'; // 📊 Pie Chart Library

class ResultView extends StatefulWidget {
  const ResultView({super.key});

  @override
  State<ResultView> createState() => _ResultViewState();
}

class _ResultViewState extends State<ResultView> {
  List elections = [];
  List results = [];
  int? selectedElectionId;
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    fetchElections();
  }

  // 🗳 Fetch Elections
  Future<void> fetchElections() async {
    final url = Uri.parse('http://192.168.0.54:8000/api/active_elections');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          elections = jsonDecode(response.body);
        });
      } else {
        showSnackBar("Failed to load elections.");
      }
    } catch (e) {
      showSnackBar("Error: $e");
    }
  }

  // 📊 Fetch Election Results
  Future<void> fetchResults(int electionId) async {
    setState(() {
      isLoading = true;
      results = [];
    });

    final url = Uri.parse('http://192.168.0.54:8000/api/election_results/$electionId');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          results = jsonDecode(response.body);
        });
      } else {
        showSnackBar("Failed to load results.");
      }
    } catch (e) {
      showSnackBar("Error: $e");
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Election Results")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Select Election:",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            DropdownButtonFormField<int>(
              value: selectedElectionId,
              hint: const Text("Choose an Election"),
              onChanged: (int? newElectionId) {
                setState(() {
                  selectedElectionId = newElectionId;
                  results = [];
                });
                if (newElectionId != null) {
                  fetchResults(newElectionId);
                }
              },
              items: elections.map<DropdownMenuItem<int>>((election) {
                return DropdownMenuItem<int>(
                  value: election['id'],
                  child: Text(election['name']),
                );
              }).toList(),
            ),
            const SizedBox(height: 20),

            // Show Pie Chart
            if (results.isNotEmpty) buildPieChart(),

            if (isLoading)
              const Center(child: CircularProgressIndicator()),

            if (!isLoading && results.isNotEmpty)
              Expanded(
                child: ListView.builder(
                  itemCount: results.length,
                  itemBuilder: (context, index) {
                    final candidate = results[index];
                    return Card(
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundImage: NetworkImage(
                            candidate['profile_picture'].isNotEmpty
                                ? 'http://192.168.0.54:8000${candidate['profile_picture']}'
                                : 'https://via.placeholder.com/150',
                          ),
                        ),
                        title: Text(candidate['name']),
                        subtitle: Text("Votes: ${candidate['vote_count']}"),
                        trailing: Icon(
                          index == 0 ? Icons.emoji_events : Icons.how_to_vote,
                          color: index == 0 ? Colors.amber : Colors.grey,
                        ),
                      ),
                    );
                  },
                ),
              ),

            if (!isLoading && results.isEmpty)
              const Center(child: Text("No results available.")),
          ],
        ),
      ),
    );
  }

  // 📊 Build Pie Chart Widget
  Widget buildPieChart() {
    return SizedBox(
      height: 300,
      child: PieChart(
        PieChartData(
          sections: results.map<PieChartSectionData>((candidate) {
            return PieChartSectionData(
              value: candidate['vote_count'].toDouble(),
              title: candidate['name'],
              color: Colors.primaries[results.indexOf(candidate) % Colors.primaries.length], // Dynamic color
              radius: 50,
              titleStyle: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
            );
          }).toList(),
          sectionsSpace: 2,
          centerSpaceRadius: 40,
        ),
      ),
    );
  }
}
