
using System;
using Quaver.API.Replays;

class Program {
	static void Main(string[] args) {
        // Get the directory where the executable is located
        string exeDirectory = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
        
        // Construct the full path to the text file
        string executableDirectory = AppDomain.CurrentDomain.BaseDirectory;
        string parentDirectory = Directory.GetParent(executableDirectory).FullName;
        parentDirectory = Directory.GetParent(parentDirectory).FullName;
        parentDirectory = Directory.GetParent(parentDirectory).FullName;
        parentDirectory = Directory.GetParent(parentDirectory).FullName;
        string filePath = Path.Combine(parentDirectory, "pepperonipeesah_-_orgt_-_DESTINY_-_Salmon.qr");

        Console.WriteLine(filePath);
        
		Replay replay = new Replay(filePath);
		Console.WriteLine(replay);
	}
}
