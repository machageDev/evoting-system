import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class ResultView extends StatelessWidget {
  final Map<String, Map<String, int>> electionResults = {
    "Presidential Election": {
      "Alice Johnson": 450,
      "Bob Smith": 320,
      "Charlie Brown": 230,
    },
    "Senate Election": {
      "David Green": 540,
      "Emma White": 460,
    }
  };

  ResultView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("All Election Results"),
        backgroundColor: Colors.blueAccent,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: electionResults.entries.map((election) {
            return Card(
              margin: const EdgeInsets.symmetric(vertical: 10),
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Text(
                      election.key,
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            color: Colors.blueAccent,
                            fontWeight: FontWeight.bold,
                          ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    SizedBox(
                      height: 250,
                      child: PieChart(
                        PieChartData(
                          sections: election.value.entries.map((candidate) {
                            return PieChartSectionData(
                              color: _getRandomColor(candidate.key),
                              value: candidate.value.toDouble(),
                              title: "${candidate.value} votes",
                              radius: 50,
                              titleStyle: const TextStyle(
                                  fontSize: 14, fontWeight: FontWeight.bold),
                            );
                          }).toList(),
                          sectionsSpace: 2,
                          centerSpaceRadius: 40,
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    Column(
                      children: election.value.entries.map((candidate) {
                        return ListTile(
                          title: Text(candidate.key,
                              style: const TextStyle(
                                  fontWeight: FontWeight.bold)),
                          trailing: Chip(
                            label: Text("${candidate.value} votes"),
                            backgroundColor: Colors.green.shade200,
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            );
          }).toList(),
        ),
      ),
    );
  }

  Color _getRandomColor(String key) {
    final List<Color> colors = [
      Colors.redAccent,
      Colors.greenAccent,
      Colors.blueAccent,
      Colors.purpleAccent,
      Colors.orangeAccent
    ];
    return colors[key.hashCode % colors.length];
  }
}
