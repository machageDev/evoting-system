import 'package:flutter/material.dart';

class ProfileView extends StatelessWidget {
  final Map<String, dynamic> user;

  const ProfileView({super.key, required this.user});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("User Profile")),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Container(
          padding: EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(10),
            boxShadow: [BoxShadow(color: Colors.grey.shade300, blurRadius: 5)],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Profile Picture Section
              CircleAvatar(
                radius: 75,
                backgroundImage: user["profile_picture"] != null
                    ? NetworkImage(user["profile_picture"])
                    : AssetImage("assets/images/default_profile.jpg") as ImageProvider,
                backgroundColor: Colors.grey.shade200,
              ),
              SizedBox(height: 10),
              Text(
                "${user["first_name"]} ${user["last_name"]}",
                style: Theme.of(context).textTheme.titleLarge,
              ),
              Text(
                user["username"],
                style: TextStyle(color: Colors.grey),
              ),
              SizedBox(height: 20),

              // Personal Information Section
              _buildInfoSection(
                icon: Icons.person,
                title: "Personal Information",
                content: Column(
                  children: [
                    _infoRow("First Name", user["first_name"]),
                    _infoRow("Last Name", user["last_name"]),
                    _infoRow("Email", user["email"]),
                    _infoRow("Phone Number", user["phone_number"]),
                  ],
                ),
              ),
              SizedBox(height: 20),

              // Account Information Section
              _buildInfoSection(
                icon: Icons.lock,
                title: "Account Information",
                content: Column(
                  children: [
                    _infoRow("Username", user["username"]),
                    _infoRow("Last Login", user["last_login"]),
                    _infoRow("Account Created", user["date_joined"]),
                  ],
                ),
              ),

              SizedBox(height: 30),
              // Edit Profile Button
              ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, "/edit_profile"); // Adjust route accordingly
                },
                child: Text("Edit Profile"),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInfoSection({required IconData icon, required String title, required Widget content}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, color: Colors.blue),
            SizedBox(width: 8),
            Text(title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
        Divider(),
        content,
      ],
    );
  }

  Widget _infoRow(String label, String value) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: TextStyle(fontWeight: FontWeight.w500)),
          Text(value, style: TextStyle(color: Colors.blueGrey)),
        ],
      ),
    );
  }
}
