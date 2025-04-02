import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ManageElectionsView extends StatefulWidget {
  const ManageElectionsView({super.key});

  @override
  _ManageElectionsViewState createState() => _ManageElectionsViewState();
}

class _ManageElectionsViewState extends State<ManageElectionsView> {
  List<Map<String, dynamic>> elections = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchElections();
  }

  Future<void> fetchElections() async {
    final url = Uri.parse('http://192.168.0.27:8000/apielection');
    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);

        setState(() {
          if (responseData is Map<String, dynamic> && responseData.containsKey('elections')) {
            elections = List<Map<String, dynamic>>.from(responseData['elections']);
          } else if (responseData is List) {
            elections = List<Map<String, dynamic>>.from(responseData);
          } else {
            showSnackBar('Unexpected response format: ${response.body}');
          }
          isLoading = false;
        });
      } else {
        showSnackBar('Failed to load elections');
      }
    } catch (e) {
      print('Error: $e');
      showSnackBar('Error fetching elections');
    }
  }

  void showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Manage Elections")),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(16.0),
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal, // Allows horizontal scrolling
                child: DataTable(
                  columns: const [
                    DataColumn(label: Text('Election Name', style: TextStyle(fontWeight: FontWeight.bold))),
                    DataColumn(label: Text('Date', style: TextStyle(fontWeight: FontWeight.bold))),
                    DataColumn(label: Text('Status', style: TextStyle(fontWeight: FontWeight.bold))),
                  ],
                  rows: elections.map((election) {
                    return DataRow(cells: [
                      DataCell(Text(election['name'] ?? 'N/A')),
                      DataCell(Text(election['election_date'] ?? 'N/A')),
                      DataCell(Text(election['status'] ?? 'N/A')),
                    ]);
                  }).toList(),
                ),
              ),
            ),
    );
  }
}