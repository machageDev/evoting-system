import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class CreateCandidateView extends StatefulWidget {
  const CreateCandidateView({super.key});

  @override
  CreateCandidateViewState createState() => CreateCandidateViewState();
}


class CreateCandidateViewState extends State<CreateCandidateView> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _positionController = TextEditingController();
  File? _image;
  final picker = ImagePicker();

  // 📸 Pick Image from Gallery
  Future<void> _pickImage() async {
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  
  Future<void> _uploadCandidate() async {
    var request = http.MultipartRequest("POST", Uri.parse("http://127.0.0.1:8000/apicreate_candidate"));

    // Attach Form Data
    request.fields["name"] = _nameController.text;
    request.fields["position"] = _positionController.text;
    request.fields["election"] = "1"; 

    // Attach Image
    if (_image != null) {
      request.files.add(
        await http.MultipartFile.fromPath(
          "profile_picture",
          _image!.path,
          contentType: MediaType("image", "jpeg"),
        ),
      );
    }

    var response = await request.send();
    
    if (response.statusCode == 201) {
      debugPrint("✅ Candidate Registered Successfully!"); 
    } else {
      debugPrint("❌ Error: ${response.reasonPhrase}");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Register Candidate")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Register a Candidate", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),

            
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: "Name"),
            ),
            const SizedBox(height: 10),

            // Position Field
            TextField(
              controller: _positionController,
              decoration: const InputDecoration(labelText: "Position"),
            ),
            const SizedBox(height: 10),

            // Image Preview
            _image == null
                ? const Text("No image selected.", style: TextStyle(color: Colors.grey))
                : Image.file(_image!, height: 150),

            const SizedBox(height: 10),

            
            ElevatedButton.icon(
              onPressed: _pickImage,
              icon: const Icon(Icons.image),
              label: const Text("Pick Image"),
            ),

            const SizedBox(height: 20),

            
            ElevatedButton.icon(
              onPressed: _uploadCandidate,
              icon: const Icon(Icons.upload),
              label: const Text("Register Candidate"),
            ),
          ],
        ),
      ),
    );
  }
}
