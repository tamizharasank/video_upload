-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 05, 2018 at 02:56 PM
-- Server version: 5.7.23-0ubuntu0.16.04.1
-- PHP Version: 7.0.30-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `videos`
--

-- --------------------------------------------------------

--
-- Table structure for table `instruction_set`
--

CREATE TABLE `instruction_set` (
  `id` int(11) NOT NULL,
  `instruction_name` varchar(200) NOT NULL,
  `uploaded_by` varchar(200) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_from` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `train`
--

CREATE TABLE `train` (
  `id` int(11) NOT NULL,
  `instruction_id` varchar(255) NOT NULL,
  `instruction_name` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `kill_id` varchar(255) NOT NULL,
  `dis` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `training_images`
--

CREATE TABLE `training_images` (
  `id` int(11) NOT NULL,
  `instruction_id` int(11) NOT NULL,
  `video_id` int(11) NOT NULL,
  `image_path` varchar(200) NOT NULL,
  `label_name` varchar(200) NOT NULL,
  `order_n` varchar(200) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_from` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `video_collection`
--

CREATE TABLE `video_collection` (
  `id` int(11) NOT NULL,
  `instruction_id` int(11) NOT NULL,
  `video_path` varchar(200) NOT NULL,
  `no_images` varchar(200) NOT NULL,
  `label_name` varchar(200) NOT NULL,
  `order_n` varchar(200) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_from` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` varchar(100) NOT NULL,
  `duration` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `instruction_set`
--
ALTER TABLE `instruction_set`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `train`
--
ALTER TABLE `train`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `training_images`
--
ALTER TABLE `training_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instruction_id` (`instruction_id`);

--
-- Indexes for table `video_collection`
--
ALTER TABLE `video_collection`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instruction_id` (`instruction_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `instruction_set`
--
ALTER TABLE `instruction_set`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `train`
--
ALTER TABLE `train`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `training_images`
--
ALTER TABLE `training_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18975;
--
-- AUTO_INCREMENT for table `video_collection`
--
ALTER TABLE `video_collection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `training_images`
--
ALTER TABLE `training_images`
  ADD CONSTRAINT `training_images_ibfk_1` FOREIGN KEY (`instruction_id`) REFERENCES `instruction_set` (`id`);

--
-- Constraints for table `video_collection`
--
ALTER TABLE `video_collection`
  ADD CONSTRAINT `video_collection_ibfk_1` FOREIGN KEY (`instruction_id`) REFERENCES `instruction_set` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
