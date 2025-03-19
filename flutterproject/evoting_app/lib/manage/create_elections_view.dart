import 'package:flutter/material.dart';

class CreateElectionsView extends StatefulWidget {
  const CreateElectionsView({super.key});

  @override
  CreateElectionsViewState createState() => CreateElectionsViewState();
}

class CreateElectionsViewState extends State<CreateElectionsView> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _dateController = TextEditingController();
  final TextEditingController _timeController = TextEditingController();
  String _status = 'pending';

  // Function to pick a date
  Future<void> _pickDate() async {
    DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2000),
      lastDate: DateTime(2101),
    );

    if (pickedDate != null) {
      setState(() {
        _dateController.text = pickedDate.toString().split(" ")[0]; // Format YYYY-MM-DD
      });
    }
  }

  // Function to pick a time
  Future<void> _pickTime() async {
    TimeOfDay? pickedTime = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );

    if (pickedTime != null) {
      setState(() {
        _timeController.text = pickedTime.format(context);
      });
    }
  }

  Future<void> _createElection() async {
    String name = _nameController.text.trim();
    String date = _dateController.text.trim();
    String time = _timeController.text.trim();

    if (name.isEmpty || date.isEmpty || time.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please fill all fields")),
      );
      return;
    }

    // Simulate API call (Replace this with actual API request)
    print("Election Created!");
    print("Name: $name");
    print("Date: $date");
    print("Time: $time");
    print("Status: $_status");

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Election '$name' created successfully!")),
    );
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
            // Election Name
            const Text("Election Name", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(hintText: "Enter election name"),
            ),
            const SizedBox(height: 16),

            // Election Date Picker
            const Text("Election Date", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            TextField(
              controller: _dateController,
              readOnly: true,
              decoration: const InputDecoration(hintText: "Select election date"),
              onTap: _pickDate,
            ),
            const SizedBox(height: 16),

            // Election Time Picker
            const Text("Election Time", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            TextField(
              controller: _timeController,
              readOnly: true,
              decoration: const InputDecoration(hintText: "Select election time"),
              onTap: _pickTime,
            ),
            const SizedBox(height: 16),

            // Election Status Dropdown
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

            // Create Election Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _createElection,
                child: const Text("Create Election"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
