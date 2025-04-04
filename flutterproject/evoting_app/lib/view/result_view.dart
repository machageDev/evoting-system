import 'package:evoting_app/Api/api_service.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class ResultView extends StatefulWidget {
  const ResultView({super.key, required Map electionResults});

  @override
  State<ResultView> createState() => _ResultViewState();
}

class _ResultViewState extends State<ResultView> {
  Map<String, Map<String, int>> electionResults = {};
  bool isLoading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    loadResults();
  }

  Future<void> loadResults() async {
    try {
      final results = await fetchElectionResults();
      setState(() {
        electionResults = results;
        isLoading = false;
      });
    } catch (e) {
      print("Error occurred while fetching results: $e");
      setState(() {
        error = e.toString();
        isLoading = false;
      });
    }
  }

  Widget _buildChart(Map<String, int> results) {
    List<PieChartSectionData> sections = results.entries.map((entry) {
      return PieChartSectionData(
        title: "${entry.value} votes",
        value: entry.value.toDouble(),
        color: Colors.blue,
        radius: 50,
        titleStyle: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.white),
      );
    }).toList();

    return PieChart(
      PieChartData(
        sections: sections,
        centerSpaceRadius: 40,
        sectionsSpace: 2,
        borderData: FlBorderData(show: false),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("All Election Results"),
        backgroundColor: Colors.blue,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: isLoading
            ? Center(child: CircularProgressIndicator())
            : error != null
                ? Center(child: Text("Error: $error"))
                : electionResults.isNotEmpty
                    ? ListView(
                        children: electionResults.entries.map((entry) {
                          String election = entry.key;
                          Map<String, int> results = entry.value;
                          return Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                election,
                                style: TextStyle(
                                  fontSize: 22,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blueAccent,
                                ),
                              ),
                              SizedBox(height: 10),
                              Container(
                                height: 300,
                                padding: EdgeInsets.all(10),
                                child: _buildChart(results),
                              ),
                              ...results.entries.map((result) => ListTile(
                                    title: Text(result.key,
                                        style: TextStyle(fontWeight: FontWeight.bold)),
                                    trailing: Chip(
                                      label: Text("${result.value} votes"),
                                      backgroundColor: Colors.green,
                                      labelStyle: TextStyle(color: Colors.white),
                                    ),
                                  )),
                              Divider(),
                            ],
                          );
                        }).toList(),
                      )
                    : Center(
                        child: Text("No active elections or results to display.",
                            style: TextStyle(color: Colors.grey)),
                      ),
      ),
    );
  }
}