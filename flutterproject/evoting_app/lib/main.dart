import 'package:evoting_app/screens/profile_view.dart';
import 'package:evoting_app/settings/settings_view.dart';
import 'package:evoting_app/widgets/custom_buttons.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '/Api/api_service.dart';
import 'manage/create_candidate_view.dart';
import '/manage/create_elections_view.dart';
import 'screens/login_view.dart';
import 'screens/register_view.dart';
import 'screens/forgot_password_view.dart';
import 'home/dashboard_view.dart';
import 'home/homepage_view.dart';
import 'home/voterdashboard_view.dart';
import 'view/result_view.dart';
import 'view/vote_view.dart';
import 'manage/manageelection_view.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'eVoting System',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        textTheme: GoogleFonts.nunitoTextTheme(),
        scaffoldBackgroundColor: Colors.grey[200], 
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue, // ✅ Button Color
            foregroundColor: Colors.white, // ✅ Button Text Color
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
          ),
        ),
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginView(),
        '/register': (context) => const RegisterView(),
        '/forgot-password': (context) => const ForgotPasswordView(),
        '/dashboard': (context) => DashboardView(),
        '/create_candidate': (context) => const CreateCandidateView(),
        '/create_elections': (context) => CreateElectionsView(),
        '/homepage_view': (context) => HomePageView(),
        '/voterdashboard_view':(context) => VoterDashboardView(),
        '/result_view': (context) => ResultView(electionResults: {},),
        '/vote_view': (context) => VoteView(),
        '/manageelection_view': (context) => ManageElectionsView(),
        '/profile':(context) =>  const ProfileView(user: {},),
        '/custom_buttons':(context) =>  const CustomButtonsDemo(),
        '/settings':(context) => const SettingsView(),
      },

      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService apiService = ApiService();
  late Future<String> futureData; // ✅ Define future variable

  @override
  void initState() {
    super.initState();
    futureData = apiService.fetchData(); 
  }
  
  @override
  Widget build(BuildContext context) {
    
    throw UnimplementedError();
  }

}
 


// ✅ Theme Data for Light and Dark Mode
final ThemeData lightTheme = ThemeData(
  brightness: Brightness.light,
  primaryColor: Colors.blue,
  scaffoldBackgroundColor: Colors.white,
  appBarTheme: const AppBarTheme(
    backgroundColor: Colors.blue,
    titleTextStyle: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
    iconTheme: IconThemeData(color: Colors.white),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: Colors.blue,
      foregroundColor: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
  ),
  textTheme: const TextTheme(
    bodyLarge: TextStyle(fontSize: 18, color: Colors.black),
    bodyMedium: TextStyle(fontSize: 16, color: Colors.black54),
  ),
);

final ThemeData darkTheme = ThemeData(
  brightness: Brightness.dark,
  primaryColor: Colors.teal,
  scaffoldBackgroundColor: Colors.black,
  appBarTheme: const AppBarTheme(
    backgroundColor: Colors.teal,
    titleTextStyle: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
    iconTheme: IconThemeData(color: Colors.white),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: Colors.teal,
      foregroundColor: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
  ),
  textTheme: const TextTheme(
    bodyLarge: TextStyle(fontSize: 18, color: Colors.white),
    bodyMedium: TextStyle(fontSize: 16, color: Colors.white70),
  ),
);
