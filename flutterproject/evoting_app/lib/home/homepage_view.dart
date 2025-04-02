// ignore_for_file: deprecated_member_use



import 'package:evoting_app/Api/api_service.dart';
import 'package:flutter/material.dart';

class HomePageView extends StatefulWidget {
  const HomePageView({super.key});

  @override
  State<HomePageView> createState() => _HomePageViewState();
}

class _HomePageViewState extends State<HomePageView> {
  String welcomeMessage = "Welcome to the eVoting System"; // Default message
  bool isLoading = false;
  String pageTitle = "Loading..."; // Title of the home page
  String aboutSystem = "Loading..."; // About system text

  @override
  void initState() {
    super.initState();
    fetchHomePageData(); 
  }

  // Function to call your API via ApiService
  Future<void> fetchHomePageData() async {
    setState(() {
      isLoading = true;
    });

    // Fetch home page data from ApiService
    ApiService apiService = ApiService();
    try {
      Map<String, dynamic> homePageData = await apiService.fetchHomePageData();

      setState(() {
        // Update the UI with the fetched data
        welcomeMessage = homePageData['welcome_message'] ?? 'Welcome to the eVoting System';
        pageTitle = homePageData['home_page_title'] ?? 'Home Page';
        aboutSystem = homePageData['about_system'] ?? '';
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        welcomeMessage = 'Failed to load home page data';
        isLoading = false;
      });
      print("Error fetching home page data: $e" );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/images/voting_background.jpg"),
            fit: BoxFit.cover,
          ),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.6),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Column(
                  children: [
                    isLoading
                        ? const CircularProgressIndicator(
                            color: Colors.white,
                          )
                        : Text(
                            welcomeMessage,
                            style: Theme.of(context)
                                .textTheme
                                .headlineMedium
                                ?.copyWith(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),
                            textAlign: TextAlign.center,
                          ),
                    const SizedBox(height: 10),
                    Text(
                      "Your secure and efficient platform for online voting.",
                      style:
                          Theme.of(context).textTheme.titleMedium?.copyWith(
                                color: Colors.white70,
                              ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.pushNamed(context, "/login");
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blueAccent,
                        padding: const EdgeInsets.symmetric(
                            horizontal: 30, vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: const Text(
                        "Log In",
                        style: TextStyle(color: Colors.white, fontSize: 18),
                      ),
                    ),
                    const SizedBox(height: 15),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.pushNamed(context, "/dashboard");
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        padding: const EdgeInsets.symmetric(
                            horizontal: 30, vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: const Text(
                        "Dashboard",
                        style: TextStyle(color: Colors.white, fontSize: 18),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 30),
              Container(
                width: MediaQuery.of(context).size.width * 0.85,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.9),
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 8,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    Text(
                      pageTitle,
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            color: Colors.black,
                            fontWeight: FontWeight.bold,
                          ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 10),
                    Text(
                      aboutSystem,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: Colors.black87,
                            fontSize: 16,
                          ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

extension on ApiService {
  fetchHomePageData() {}
}
