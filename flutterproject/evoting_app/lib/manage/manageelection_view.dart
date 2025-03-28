// ignore_for_file: library_private_types_in_public_api

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
    final url = Uri.parse('http://192.168.0.28:8000/api_get_election');
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

  void showEditModal(Map election) {
    TextEditingController nameController = TextEditingController(text: election['name']);
    TextEditingController dateController = TextEditingController(text: election['election_date']);
    String status = election['status'];

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text("Edit Election"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: nameController, decoration: InputDecoration(labelText: "Election Name")),
              TextField(controller: dateController, decoration: InputDecoration(labelText: "Election Date")),
              DropdownButtonFormField(
                value: status,
                onChanged: (value) => setState(() => status = value!),
                items: ['pending', 'active', 'completed']
                    .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                    .toList(),
              ),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: Text("Cancel")),
            ElevatedButton(
              onPressed: () {
                updateElection(election['id'], nameController.text, dateController.text, status);
                Navigator.pop(context);
              },
              child: Text("Save Changes"),
            ),
          ],
        );
      },
    );
  }

  Future<void> updateElection(int id, String name, String date, String status) async {
    final url = Uri.parse('http://192.168.0.54:8000/api/edit_election/$id/');
    final response = await http.post(url, body: {'name': name, 'election_date': date, 'status': status});
    if (response.statusCode == 200) {
      fetchElections();
    } else {
      print('Failed to update election');
    }
  }

  Future<void> deleteElection(int id) async {
    final url = Uri.parse('http://192.168.0.54:8000/api/delete_election/$id/');
    final response = await http.delete(url);
    if (response.statusCode == 200) {
      fetchElections();
    } else {
      print('Failed to delete election');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Manage Elections")),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                children: [
                  ElevatedButton(
                    onPressed: () => Navigator.pushNamed(context, '/create_elections'),
                    child: Text("Create New Election"),
                  ),
                  Expanded(
                    child: ListView.builder(
                      itemCount: elections.length,
                      itemBuilder: (context, index) {
                        final election = elections[index];
                        return Card(
                          child: ListTile(
                            title: Text(election['name'], style: TextStyle(fontWeight: FontWeight.bold)),
                            subtitle: Text("Date: ${election['election_date']}, Status: ${election['status']}"),
                            trailing: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                IconButton(icon: Icon(Icons.edit), onPressed: () => showEditModal(election)),
                                IconButton(icon: Icon(Icons.delete), onPressed: () => deleteElection(election['id'])),
                              ],
                            ),
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
