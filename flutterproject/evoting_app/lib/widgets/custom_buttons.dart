import 'package:flutter/material.dart';

class CustomButtonsDemo extends StatelessWidget {
  const CustomButtonsDemo({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Custom Buttons")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // ✅ Circular Button (Default)
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                shape: const CircleBorder(),
                padding: const EdgeInsets.all(20),
                backgroundColor: Colors.blue,
              ),
              child: const Icon(Icons.check, size: 20, color: Colors.white),
            ),
            const SizedBox(height: 16),

            // ✅ Small Circular Button
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                shape: const CircleBorder(),
                padding: const EdgeInsets.all(12),
                backgroundColor: Colors.green,
              ),
              child: const Icon(Icons.check, size: 14, color: Colors.white),
            ),
            const SizedBox(height: 16),

            // ✅ Large Circular Button
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                shape: const CircleBorder(),
                padding: const EdgeInsets.all(28),
                backgroundColor: Colors.red,
              ),
              child: const Icon(Icons.check, size: 26, color: Colors.white),
            ),
            const SizedBox(height: 32),

            // ✅ Icon-Split Button
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.download, color: Colors.white),
              label: const Text("Download"),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                backgroundColor: Colors.blue,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
            const SizedBox(height: 16),

            // ✅ Small Icon-Split Button
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.share, size: 14, color: Colors.white),
              label: const Text("Share", style: TextStyle(fontSize: 12)),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                backgroundColor: Colors.orange,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
            const SizedBox(height: 16),

            // ✅ Large Icon-Split Button
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.upload, size: 24, color: Colors.white),
              label: const Text("Upload", style: TextStyle(fontSize: 18)),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 26, vertical: 16),
                backgroundColor: Colors.purple,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

void main() {
  runApp(const MaterialApp(home: CustomButtonsDemo()));
}
