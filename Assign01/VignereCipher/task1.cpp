#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <cctype>
#include <algorithm>

struct LetterStat
{
    char letter;
    long long count;
};

int main(int argc, char *argv[])
{
    // 1. File Input via Command-Line Arguments
    if (argc < 2)
    {
        std::cerr << "Usage: " << argv[0] << " <input_file_path>\n";
        return 1;
    }

    std::ifstream inFile(argv[1]);
    if (!inFile.is_open())
    {
        std::cerr << "Error: Could not open file '" << argv[1] << "'\n";
        return 1;
    }

    std::vector<long long> letter_counts(26, 0);
    long long total_alphabetic = 0;
    char ch;

    // 2 & 3. Case Normalization and Non-Alphabetic Filtering
    while (inFile.get(ch))
    {
        if (std::isalpha(static_cast<unsigned char>(ch)))
        {
            char upper_ch = std::toupper(static_cast<unsigned char>(ch));
            letter_counts[upper_ch - 'A']++;
            total_alphabetic++;
        }
    }

    inFile.close();

    // Populate data for sorting
    std::vector<LetterStat> stats;
    stats.reserve(26);
    for (int i = 0; i < 26; ++i)
    {
        stats.push_back({static_cast<char>('A' + i), letter_counts[i]});
    }

    // Sort descending by count (most frequent first); alphabetical tie-breaker
    std::sort(stats.begin(), stats.end(), [](const LetterStat &a, const LetterStat &b)
              {
        if (a.count != b.count) {
            return a.count > b.count;
        }
        return a.letter < b.letter; });

    // 4 & 5. Output Formatting and Relative Frequency Calculation
    std::cout << "========================================\n";
    std::cout << std::left << std::setw(8) << "Letter"
              << std::right << std::setw(12) << "Count"
              << std::setw(18) << "Frequency (%)" << "\n";
    std::cout << "========================================\n";

    for (const auto &item : stats)
    {
        double frequency_pct = (total_alphabetic > 0)
                                   ? (static_cast<double>(item.count) / total_alphabetic) * 100.0
                                   : 0.0;

        std::cout << std::left << std::setw(8) << item.letter
                  << std::right << std::setw(12) << item.count
                  << std::setw(17) << std::fixed << std::setprecision(2) << frequency_pct << "%\n";
    }

    std::cout << "========================================\n";
    std::cout << "Total Alphabetic Characters: " << total_alphabetic << "\n";

    return 0;
}