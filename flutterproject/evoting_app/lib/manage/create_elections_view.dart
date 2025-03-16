import 'package:flutter/material.dart';


class CreateElectionsView extends StatefulWidget {
  const CreateElectionsView({super.key});

  @override
  CreateElectionsViewState createState() => CreateElectionsViewState();
}

class CreateElectionsViewState extends State<CreateElectionsView> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _dateController = TextEditingController();
  String _status = 'pending';

  Future<void> _createElection() async {
    String name = _nameController.text.trim();
    String date = _dateController.text.trim();

    if (name.isEmpty || date.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please fill all fields")),
      );
      return;
    }
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Create Election")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Election Name", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(hintText: "Enter election name"),
            ),
            const SizedBox(height: 16),
            const Text("Election Date", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            TextField(
              controller: _dateController,
              decoration: const InputDecoration(hintText: "Enter election date (YYYY-MM-DD)"),
            ),
            const SizedBox(height: 16),
            const Text("Election Status", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            DropdownButtonFormField<String>(
              value: _status,
              onChanged: (newValue) {
                setState(() {
                  _status = newValue!;
                });
              },
              items: const [
                DropdownMenuItem(value: "pending", child: Text("Pending")),
                DropdownMenuItem(value: "active", child: Text("Active")),
              ],
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _createElection,
              child: const Text("Create Election"),
            ),
          ],
        ),
      ),
    );
  }
}
