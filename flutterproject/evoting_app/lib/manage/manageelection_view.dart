import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ManageElectionsView extends StatefulWidget {
  const ManageElectionsView({super.key});

  @override
  _ManageElectionsViewState createState() => _ManageElectionsViewState();
}

class _ManageElectionsViewState extends State<ManageElectionsView> {
  List elections = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchElections();
  }

  Future<void> fetchElections() async {
    final url = Uri.parse('http://192.168.0.102:8000/api_get_election');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          elections = json.decode(response.body);
          isLoading = false;
        });
      } else {
        print('Failed to load elections: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching elections: $e');
    }
  } 

  void showEditDialog(Map election) {
    TextEditingController nameController = TextEditingController(text: election['name']);
    TextEditingController dateController = TextEditingController(text: election['election_date']);
    String status = election['status'];

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text("Edit Election"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: const InputDecoration(labelText: "Election Name"),
              ),
              TextField(
                controller: dateController,
                decoration: const InputDecoration(labelText: "Election Date"),
              ),
              DropdownButtonFormField(
                value: status,
                items: ['pending', 'active', 'completed'].map((s) {
                  return DropdownMenuItem(value: s, child: Text(s.capitalize()));
                }).toList(),
                onChanged: (value) => setState(() => status = value!),
              )
            ],
          ),      
            
          
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Manage Elections")),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  ElevatedButton(
                    onPressed: () => Navigator.pushNamed(context, '/create_elections'),
                    child: const Text("Create New Election"),
                  ),
                  Expanded(
                    child: ListView.builder(
                      itemCount: elections.length,
                      itemBuilder: (context, index) {
                        final election = elections[index];
                        return Card(
                          child: ListTile(
                            title: Text(election['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                            subtitle: Text("Date: ${election['election_date']}, Status: ${election['status']}"),
                           
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}

extension StringExtension on String {
  String capitalize() {
    return this[0].toUpperCase() + substring(1);
  }
}