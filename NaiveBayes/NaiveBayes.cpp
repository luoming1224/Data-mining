// NaiveBayes.cpp : 
//

// NaiveBayes.cpp : 
//

//#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <set>
using namespace std;

string data[15][6];
set<string>		stringset;
map< string, set<string> >  stringmap;

vector<string*>		yClassData;
vector<string*>		nClassData;

void readDataFile(const char* filePath)
{
	char buffer[255];
	ifstream myfile(filePath);
	if (myfile)
	{
		int index = 0;
		while (!myfile.eof())
		{
			myfile.getline(buffer, 255);
			string strtmp = buffer;
			int subindex = 0;
			while(strtmp != "")
			{
				int pos = strtmp.find(" ");
				if (pos != string::npos)
				{
					string sdata = strtmp.substr(0, pos);
					data[index][subindex++] = sdata;
					strtmp = strtmp.substr(pos+1);
				}
				else
				{
					string sdata;
					int n = strtmp.length();
					if(strtmp[n-1] == '\r')
						sdata = strtmp.substr(0, n-1);
					else
						sdata = strtmp.substr(0);
					data[index][subindex++] = sdata;
					strtmp = "";
				}
			}
			index++;
		}
	}
	myfile.close();

	for (int i = 0; i < 15; i++)
	{
		for (int j = 0; j < 6; j++)
		{
			printf(" %s ", data[i][j].c_str());
		}
		printf("\n");
	}
	printf("\n");

}

void initAttrValue()
{
	for (int j = 1; j < 6; j++)
	{
		stringset.clear();
		for (int i = 1; i < 15; i++)
		{
			stringset.insert(data[i][j]);
		}
		string key = data[0][j];
		stringmap[key] = stringset;
	}

	map< string, set<string> >::iterator it = stringmap.begin();
	map< string, set<string> >::iterator end = stringmap.end();
	for (; it != end; it++)
	{
		printf("%s ", (it->first).c_str());
		set<string>::iterator it1 = it->second.begin();
		set<string>::iterator end1 = it->second.end();
		for (; it1 != end1; ++it1)
		{
			printf("%s ", (*it1).c_str());
		}
		printf("\n");
	}

	for (int i = 1; i < 15; i++)
	{
		if (data[i][5] == "Yes")
		{
			yClassData.push_back(data[i]);
		}
		else
			nClassData.push_back(data[i]);
	}
}

int getConditionAttrName(string condition)
{
	string attrName = "";
	int attrIndex = 1;
	map< string, set<string> >::iterator it = stringmap.begin();
	map< string, set<string> >::iterator end = stringmap.end();
	for (; it != end; it++)
	{
		if ((it->second.count(condition) == 1) && (it->first != "BuysComputer"))
		{
			attrName = it->first;
			break;
		}
	}
	for (int j = 0; j < 5; j++)
	{
		if (data[0][j] == attrName)
		{
			attrIndex = j;
			break;
		}
	}
	return attrIndex;
}

double computeConditionProbably(string condition, string classType)
{
	int count = 0;
	int attrIndex = 1;

	if (condition == "")
	{
		if (classType == "Yes")
		{
			return 1.0 * yClassData.size() / 14;
		}
		else
			return 1.0 * nClassData.size() / 14;
	}

	attrIndex = getConditionAttrName(condition);
	vector<string*>::iterator it;
	if (classType == "Yes")
	{
		it = yClassData.begin();
		for (; it != yClassData.end(); ++it)
		{
			if ((*it)[attrIndex] == condition)
			{
				count++;
			}
		}
		return 1.0 * count / yClassData.size();
	}
	else
	{
		it = nClassData.begin();
		for (; it != nClassData.end(); ++it)
		{
			if ((*it)[attrIndex] == condition)
			{
				count++;
			}
		}
		return 1.0 * count / nClassData.size();
	}

}

string naiveBayesClassificate(string data)
{
	vector<string> dataFeatures;

	double xWhenYes = 1.0;
	double xWhenNo = 1.0;
	double pYes = 1;
	double pNo = 1;

	string strtmp = data;
	while(strtmp != "")
	{
		int pos = strtmp.find(" ");
		if (pos != string::npos)
		{
			string sdata = strtmp.substr(0, pos);
			dataFeatures.push_back(sdata);
			strtmp = strtmp.substr(pos+1);
		}
		else
		{
			string sdata = strtmp.substr(0);
			dataFeatures.push_back(sdata);
			strtmp = "";
		}
	}

	int nsize = dataFeatures.size();
	for (int i = 0; i < nsize; i++)
	{
		xWhenYes *= computeConditionProbably(dataFeatures[i], "Yes");
		xWhenNo *= computeConditionProbably(dataFeatures[i], "No");
	}

	pYes = xWhenYes * computeConditionProbably("", "Yes");
	pNo = xWhenNo * computeConditionProbably("", "No");

	printf("YES[%lf]   NO[%lf]\n", pYes, pNo);

	return (pYes > pNo ? "Yes" : "No");
}

int main(int argc, char* argv[])
{
	printf("%d  %s\n", argc, argv);
	readDataFile("D:\\input.txt");
	initAttrValue();

	string testData = "Youth Medium Yes Fair";

	string ret = naiveBayesClassificate(testData);

	printf("%s\n", ret.c_str());

	system("pause");
	return 0;
}

