import {
   Button,
   VStack,
   Heading,
   Box,
   Modal,
   ModalOverlay,
   ModalContent,
   ModalHeader,
   ModalCloseButton,
   ModalBody,
   FormControl,
   FormLabel,
   Image,
   Text,
   Input,
   ModalFooter,
   useDisclosure,
   useToast,
} from "@chakra-ui/react";
// import { isDragActive } from "framer-motion";
import { useForm } from "react-hook-form";
import unisamplelogo from "../assets/START YOUR CODING JOURNEY TODAY (1).svg";
import { useCallback, useState, useRef } from "react"; // Added useRef
import { useDropzone } from "react-dropzone";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod/dist/zod.js";

const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/svg+xml"];

const schema = z.object({
   name: z.string().min(1, { message: "Name field is required" }).max(100, { message: "Name cannot exceed 100 characters" }),
   contact: z
      .string()
      .min(1, { message: "Contact field is required" })
      .regex(/^\d+$/, { message: "Contact must contain numbers only" })
      .min(11, { message: "Contact must be 11 digits" })
      .max(11, { message: "Contact must be 11 digits" }),
   email: z.string().min(1, { message: "Email is required" }).email({ message: "Invalid email address" }),
   logo: z
      .any()
      .refine((file) => file?.length !== 0, "Logo is required")
      .refine((file) => file?.[0]?.size <= MAX_FILE_SIZE, "Maximum image size is 5MB")
      .refine((file) => ACCEPTED_IMAGE_TYPES.includes(file?.[0]?.type), "Only .jpg, .jpeg, .png and .svg formats are supported"),
});

type FormInstitutionProfile = z.infer<typeof schema>;

const EditInstitutionDetail = () => {
   const initialInstitution = {
      logo: "",
      name: "Covocation University",
      contact: "07000120030",
      email: "info@exampleuniversity.edu",
   };

   const [institution, setInstitution] = useState(initialInstitution);
   const [isEditProfileOpen, setIsEditProfileOpen] = useState(false);
   const [previewImage, setPreviewImage] = useState<string | null>(null);
   const fileInputRef = useRef<HTMLInputElement>(null); // Add ref for file input

   const {
      register,
      handleSubmit,
      reset,
      setValue,
      formState: { errors },
   } = useForm<FormInstitutionProfile>({
      resolver: zodResolver(schema),
      defaultValues: institution,
   });

   const { isOpen, onOpen, onClose } = useDisclosure();
   const toast = useToast();

   const handleFileChange = (files: File[]) => {
      if (files && files[0]) {
         const file = files[0];
         // Set the file for form validation
         setValue("logo", [file], { shouldValidate: true });

         // Create preview
         const reader = new FileReader();
         reader.onload = (event) => {
            setPreviewImage(event.target?.result as string);
         };
         reader.readAsDataURL(file);
      }
   };

   const onDrop = useCallback((acceptedFiles: File[]) => {
      handleFileChange(acceptedFiles);
   }, []);

   const { getRootProps, getInputProps, isDragActive } = useDropzone({
      onDrop,
      accept: {
         "image/*": ACCEPTED_IMAGE_TYPES,
      },
      maxSize: MAX_FILE_SIZE,
      multiple: false,
      noClick: true, // Disable click from dropzone
   });

   const handleBoxClick = () => {
      if (fileInputRef.current) {
         fileInputRef.current.click();
      }
   };

   const onSubmit = (data: FormInstitutionProfile) => {
      const formData = new FormData();
      formData.append("name", data.name);
      formData.append("contact", data.contact);
      formData.append("email", data.email);
      if (data.logo?.[0]) {
         formData.append("logo", data.logo[0]);
      }

      setInstitution({
         ...data,
         logo: previewImage || institution.logo,
      });

      setIsEditProfileOpen(false);
      console.log("Form Data:", formData);
      console.log("Form Values:", data);

      toast({
         title: "Profile updated successfully!",
         status: "success",
         duration: 2000,
         isClosable: true,
         position: "top",
      });

      onClose();
   };

   const handleCloseModal = () => {
      setPreviewImage(null);
      reset();
      onClose();
   };

   return (
      <>
         <Box position="relative">
            <Button position="absolute" top={0} right={0} colorScheme="blue" onClick={onOpen}>
               Edit
            </Button>
            <VStack align="stretch" spacing={6}>
               <Heading size="lg" mb={4}>
                  Institution Details
               </Heading>
               <Image src={institution.logo || unisamplelogo} alt="Institution Logo" maxH="200px" fallbackSrc={unisamplelogo} />
               <Text>
                  <strong>Name:</strong> {institution.name}
               </Text>
               <Text>
                  <strong>Contact:</strong> {institution.contact}
               </Text>
               <Text>
                  <strong>Email:</strong> {institution.email}
               </Text>
            </VStack>
         </Box>

         <Modal isOpen={isOpen} onClose={handleCloseModal} size="xl">
            <ModalOverlay />
            <ModalContent>
               <form onSubmit={handleSubmit(onSubmit)}>
                  <ModalHeader>Edit Institution Details</ModalHeader>
                  <ModalCloseButton />
                  <ModalBody>
                     <VStack spacing={4}>
                        <Box
                           {...getRootProps()}
                           border="2px dashed"
                           borderColor={isDragActive ? "blue.500" : "gray.300"}
                           borderRadius="md"
                           p={4}
                           textAlign="center"
                           cursor="pointer"
                           w="100%"
                           onClick={handleBoxClick} // Add click handler
                        >
                           <input
                              type="file"
                              ref={fileInputRef}
                              style={{ display: "none" }}
                              accept={ACCEPTED_IMAGE_TYPES.join(",")}
                              onChange={(e) => {
                                 if (e.target.files) {
                                    handleFileChange(Array.from(e.target.files));
                                 }
                              }}
                           />
                           {previewImage ? (
                              <Image src={previewImage} alt="Institution Logo Preview" maxH="200px" />
                           ) : (
                              <Text>{isDragActive ? "Drop the logo here" : "Drag and drop institution logo here, or click to select file"}</Text>
                           )}
                        </Box>
                        {errors.logo && (
                           <Text fontSize="sm" color="red.500">
                              {errors.logo.message as string}
                           </Text>
                        )}

                        <FormControl>
                           <FormLabel>Institution Name</FormLabel>
                           <Input {...register("name")} size="lg" />
                           {errors.name && (
                              <Text fontSize="sm" color="red.500">
                                 {errors.name.message}
                              </Text>
                           )}
                        </FormControl>

                        <FormControl>
                           <FormLabel>Phone</FormLabel>
                           <Input {...register("contact")} size="lg" />
                           {errors.contact && (
                              <Text fontSize="sm" color="red.500">
                                 {errors.contact.message}
                              </Text>
                           )}
                        </FormControl>

                        <FormControl>
                           <FormLabel>Email</FormLabel>
                           <Input {...register("email")} size="lg" type="email" />
                           {errors.email && (
                              <Text fontSize="sm" color="red.500">
                                 {errors.email.message}
                              </Text>
                           )}
                        </FormControl>
                     </VStack>
                  </ModalBody>
                  <ModalFooter>
                     <Button colorScheme="blue" mr={3} type="submit">
                        Save
                     </Button>
                     <Button variant="ghost" onClick={handleCloseModal}>
                        Cancel
                     </Button>
                  </ModalFooter>
               </form>
            </ModalContent>
         </Modal>
      </>
   );
};

export default EditInstitutionDetail;
