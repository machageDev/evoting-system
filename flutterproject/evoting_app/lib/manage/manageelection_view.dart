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
  String errorMessage = '';

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
          if (responseData is List) {
            elections = List<Map<String, dynamic>>.from(responseData);
          } else if (responseData is Map<String, dynamic>) {
            elections = [responseData]; // Wrap single object inside a list
          } else {
            errorMessage = 'Unexpected response format';
          }
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Failed to load elections';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error fetching elections: $e';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Manage Elections")),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
              ? Center(child: Text(errorMessage, style: TextStyle(color: Colors.red, fontSize: 18)))
              : Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: DataTable(
                      border: TableBorder.all(),
                      columns: const [
                        DataColumn(label: Text('Election Name', style: TextStyle(fontWeight: FontWeight.bold))),
                        DataColumn(label: Text('Date', style: TextStyle(fontWeight: FontWeight.bold))),
                        DataColumn(label: Text('Status', style: TextStyle(fontWeight: FontWeight.bold))),
                      ],
                      rows: elections.map((election) {
                        Color statusColor;
                        String status = election['status'] ?? 'N/A';

                        // Set the color based on the status
                        if (status == 'active') {
                          statusColor = Colors.green;
                        } else if (status == 'pending') {
                          statusColor = Colors.red;
                        } else {
                          statusColor = Colors.grey;
                        }

                        return DataRow(
                          cells: [
                            DataCell(Text(election['name'] ?? 'N/A')),
                            DataCell(Text(election['date'] ?? 'N/A')), // Fixed to match your JSON
                            DataCell(
                              Text(
                                status,
                                style: TextStyle(color: statusColor), // Apply the status color
                              ),
                            ),
                          ],
                        );
                      }).toList(),
                    ),
                  ),
                ),
    );
  }
}
