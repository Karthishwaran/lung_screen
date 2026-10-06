-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 24, 2024 at 06:04 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `lungs_screener`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `recommendation`
--

CREATE TABLE `recommendation` (
  `id` int(11) NOT NULL,
  `hospital` varchar(50) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recommendation`
--

INSERT INTO `recommendation` (`id`, `hospital`, `address`, `city`) VALUES

(1, 'Adyar Cancer Institute (WIA)', 'East Canal Bank Rd, Adyar', 'Chennai'),
(2, 'Apollo Cancer Centre', '21, Greams Lane, Off Greams Road', 'Chennai'),
(3, 'MIOT International Cancer Centre', 'Mount Poonamallee Rd, Manapakkam', 'Chennai'),
(4, 'HCG Cancer Centre Chennai', 'Kamarajar Salai, Kottivakkam', 'Chennai'),
(5, 'Sri Ramachandra Medical Centre (Oncology)', 'Ramachandra Nagar, Porur', 'Chennai'),
(6, 'VS Hospitals - Advanced Cancer Care', 'East Spur Tank Road, Chetpet', 'Chennai'),
(7, 'Global Health City (Cancer Institute)', 'Perumbakkam', 'Chennai'),
(8, 'Government Royapettah Hospital (Oncology)', 'Westcott Rd, Royapettah', 'Chennai'),
(9, 'Aravind Medical Centre (Oncology)', 'Sankar Nagar', 'Tirunelveli'),
(10, 'Tirunelveli Medical College Hospital (Cancer Dept)', 'High Ground', 'Tirunelveli'),
(11, 'Meenakshi Mission Hospital & Research Centre (Oncology)', 'Lake Area, Melur Road', 'Madurai'),
(12, 'Apollo Speciality Hospitals Madurai (Cancer Care)', 'Lake View Rd, KK Nagar', 'Madurai'),
(13, 'Government Rajaji Hospital (Oncology)', 'Panagal Rd', 'Madurai'),
(14, 'Ganga Medical Centre & Hospitals (Oncology)', 'Mettupalayam Rd', 'Coimbatore'),
(15, 'PSG Hospitals (Cancer Centre)', 'Avinashi Rd, Peelamedu', 'Coimbatore'),
(16, 'KMCH Cancer Centre', 'Avinashi Rd', 'Coimbatore'),
(17, 'Kauvery Hospital (Cancer Care)', 'Tennur', 'Trichy'),
(18, 'Apollo Speciality Hospitals Trichy (Oncology)', 'Chennai Bypass Rd', 'Trichy'),
(19, 'Vinayaka Mission Hospital (Oncology)', 'NH 47, Sankari Main Rd', 'Salem'),
(20, 'Government Mohan Kumaramangalam Medical College Hospital (Cancer Dept)', 'Steel Plant Rd', 'Salem')

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `email`, `mobile`, `address`, `uname`, `pass`, `rdate`) VALUES
(1, 'Ram', 'ram@gmail.com', 9054621096, '', 'ram', '1234', ''),
(2, 'Suresh', 'suresh@gmail.com', 9845454212, '', 'suresh', '123456', ''),
(3, 'Raj', 'raj@gmail.com', 9638527414, '', 'raj', '123456', '');
